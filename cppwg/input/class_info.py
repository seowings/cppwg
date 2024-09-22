"""Class information structure."""

import logging
import os
import re
from typing import Any, Dict, List, Optional

from pygccxml.declarations.matchers import access_type_matcher_t
from pygccxml.declarations.runtime_errors import declaration_not_found_t

from cppwg.input.cpp_type_info import CppTypeInfo
from cppwg.utils import utils


class CppClassInfo(CppTypeInfo):
    """
    An information structure for individual C++ classes to be wrapped.

    Attributes
    ----------
    cpp_names : List[str]
        The C++ names of the class e.g. ["Foo<2,2>", "Foo<3,3>"]
    py_names : List[str]
        The Python names of the class e.g. ["Foo2_2", "Foo3_3"]
    decls : pygccxml.declarations.declaration_t
        Declarations for this type's base class, one per template instantiation
    """

    def __init__(self, name: str, class_config: Optional[Dict[str, Any]] = None):

        super().__init__(name, class_config)

        self.cpp_names: List[str] = None
        self.py_names: List[str] = None
        self.base_decls: Optional[List["declaration_t"]] = None  # noqa: F821

    def extract_templates_from_source(self) -> None:
        """
        Extract template args from the associated source file.

        Search the source file for a class signature matching one of the
        template signatures defined in `template_substitutions`. If a match
        is found, set the corresponding template arg replacements for the class.
        """
        # Skip if there are template args attached directly to the class
        if self.template_arg_lists:
            return

        # Skip if there is no source file
        source_path = self.source_file_full_path
        if not source_path:
            return

        # Get list of template substitutions applicable to this class
        # e.g. [ {"signature":"<int A, int B>", "replacement":[[2,2], [3,3]]} ]
        substitutions = self.hierarchy_attribute_gather("template_substitutions")

        # Skip if there are no applicable template substitutions
        if not substitutions:
            return

        source = utils.read_source_file(
            source_path,
            strip_comments=True,
            strip_preprocessor=True,
            strip_whitespace=True,
        )

        # Search for template signatures in the source file
        for substitution in substitutions:
            # Signature e.g. <int A, int B>
            signature = substitution["signature"].strip()

            class_list = utils.find_classes_in_source(
                source,
                class_name=self.name,
                template_signature=signature,
            )

            if class_list:
                self.template_signature = signature

                # Replacement e.g. [[2,2], [3,3]]
                self.template_arg_lists = substitution["replacement"]

                # Extract parameters ["A", "B"] from "<int A, int B = A>"
                self.template_params = []
                for part in signature.split(","):
                    param = (
                        part.strip()
                        .replace("<", "")
                        .replace(">", "")
                        .split(" ")[1]
                        .split("=")[0]
                        .strip()
                    )
                    self.template_params.append(param)
                break

    def is_child_of(self, other: "ClassInfo") -> bool:  # noqa: F821
        """
        Check if the class is a child of the specified class.

        Parameters
        ----------
        other : ClassInfo
            The other class to check

        Returns
        -------
        bool
            True if the class is a child of the specified class, False otherwise
        """
        if not self.base_decls:
            return False
        if not other.decls:
            return False
        return any(decl in other.decls for decl in self.base_decls)

    def requires(self, other: "ClassInfo") -> bool:  # noqa: F821
        """
        Check if the specified class is used in method signatures of this class.

        Parameters
        ----------
        other : ClassInfo
            The specified class to check.

        Returns
        -------
        bool
            True if the specified class is used in method signatures of this class.
        """
        if not self.decls:
            return False

        query = access_type_matcher_t("public")
        name_regex = re.compile(r"\b" + re.escape(other.name) + r"\b")

        for class_decl in self.decls:
            method_decls = class_decl.member_functions(function=query, allow_empty=True)
            for method_decl in method_decls:
                for arg_type in method_decl.argument_types:
                    if name_regex.search(arg_type.decl_string):
                        return True

            ctor_decls = class_decl.constructors(function=query, allow_empty=True)
            for ctor_decl in ctor_decls:
                for arg_type in ctor_decl.argument_types:
                    if name_regex.search(arg_type.decl_string):
                        return True
        return False

    def update_from_ns(self, source_ns: "namespace_t") -> None:  # noqa: F821
        """
        Update class with information from the source namespace.

        Adds the class declarations and base class declarations.

        Parameters
        ----------
        source_ns : pygccxml.declarations.namespace_t
            The source namespace
        """
        logger = logging.getLogger()

        # Skip excluded classes
        if self.excluded:
            return

        self.decls = []

        for class_cpp_name in self.cpp_names:
            class_name = class_cpp_name.replace(" ", "")  # e.g. Foo<2,2>

            try:
                class_decl = source_ns.class_(class_name)

            except declaration_not_found_t as e1:
                if (
                    self.template_signature is None
                    or "=" not in self.template_signature
                ):
                    logger.error(f"Could not find declaration for class {class_name}")
                    raise e1

                # If class has default args, try to compress the template signature
                logger.warning(
                    f"Could not find declaration for class {class_name}: trying for a partial match."
                )

                # Try to find the class without default template args
                # e.g. for template <int A, int B=A> class Foo {};
                # Look for Foo<2> instead of Foo<2,2>
                pos = 0
                for i, s in enumerate(self.template_signature.split(",")):
                    if "=" in s:
                        pos = i
                        break

                class_name = ",".join(class_name.split(",")[0:pos]) + " >"

                try:
                    class_decl = source_ns.class_(class_name)

                except declaration_not_found_t as e2:
                    logger.error(f"Could not find declaration for class {class_name}")
                    raise e2

                logger.info(f"Found {class_name}")

            self.decls.append(class_decl)

        # Update the base class declarations
        self.base_decls = [
            base.related_class for decl in self.decls for base in decl.bases
        ]

    def update_from_source(self, source_files: List[str]) -> None:
        """
        Update class with information from the source headers.
        """
        # Skip excluded classes
        if self.excluded:
            return

        # Map class to a source file, assuming the file name is the class name
        for file_path in source_files:
            file_name = os.path.basename(file_path)
            if self.name == os.path.splitext(file_name)[0]:
                self.source_file_full_path = file_path
                if self.source_file is None:
                    self.source_file = file_name

        # Extract template args from the source file
        self.extract_templates_from_source()

        # Update the C++ and Python class names
        self.update_names()

    def update_py_names(self) -> None:
        """
        Set the Python names for the class, accounting for template args.

        Set the name of the class as it will appear on the Python side. This
        collapses template arguments, separating them by underscores and removes
        special characters. The return type is a list, as a class can have
        multiple names if it is templated. For example, a class "Foo" with
        template arguments [[2, 2], [3, 3]] will have a python name list
        ["Foo2_2", "Foo3_3"].
        """
        # Handles untemplated classes
        if self.template_arg_lists is None:
            if self.name_override:
                self.py_names = [self.name_override]
            else:
                self.py_names = [self.name]
            return

        self.py_names = []

        # Table of special characters for removal
        rm_chars = {"<": None, ">": None, ",": None, " ": None}
        rm_table = str.maketrans(rm_chars)

        # Clean the type name
        type_name = self.name
        if self.name_override is not None:
            type_name = self.name_override

        # Do standard name replacements e.g. "unsigned int" -> "Unsigned"
        for name, replacement in self.name_replacements.items():
            type_name = type_name.replace(name, replacement)

        # Remove special characters
        type_name = type_name.translate(rm_table)

        # Capitalize the first letter e.g. "foo" -> "Foo"
        if len(type_name) > 1:
            type_name = type_name[0].capitalize() + type_name[1:]

        # Create a string of template args separated by "_" e.g. 2_2
        for template_arg_list in self.template_arg_lists:
            # Example template_arg_list : [2, 2]

            template_string = ""
            for idx, arg in enumerate(template_arg_list):

                # Do standard name replacements
                arg_str = str(arg)
                for name, replacement in self.name_replacements.items():
                    arg_str = arg_str.replace(name, replacement)

                # Remove special characters
                arg_str = arg_str.translate(rm_table)

                # Capitalize the first letter
                if len(arg_str) > 1:
                    arg_str = arg_str[0].capitalize() + arg_str[1:]

                # Add "_" between template arguments
                template_string += arg_str
                if idx < len(template_arg_list) - 1:
                    template_string += "_"

            self.py_names.append(type_name + template_string)

    def update_cpp_names(self) -> None:
        """
        Set the C++ names for the class, accounting for template args.

        Set the name of the class as it should appear in C++.
        The return type is a list, as a class can have multiple names
        if it is templated. For example, a class "Foo" with
        template arguments [[2, 2], [3, 3]] will have a C++ name list
        ["Foo<2,2 >", "Foo<3,3 >"].
        """
        # Handles untemplated classes
        if self.template_arg_lists is None:
            self.cpp_names = [self.name]
            return

        self.cpp_names = []
        for template_arg_list in self.template_arg_lists:
            # Create template string from arg list e.g. [2, 2] -> "<2,2 >"
            template_string = ",".join([str(arg) for arg in template_arg_list])
            template_string = "<" + template_string + " >"

            # Join full name e.g. "Foo<2,2 >"
            self.cpp_names.append(self.name + template_string)

    def update_names(self) -> None:
        """
        Update the C++ and Python names for the class.
        """
        self.update_cpp_names()
        self.update_py_names()

    @property
    def parent(self) -> "ModuleInfo":  # noqa: F821
        """
        Returns the parent module info object.
        """
        return self.module_info
