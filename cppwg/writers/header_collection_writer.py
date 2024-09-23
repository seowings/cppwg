"""Writer for header collection hpp file."""

import os
from typing import Dict

from cppwg.input.class_info import CppClassInfo
from cppwg.input.free_function_info import CppFreeFunctionInfo
from cppwg.input.package_info import PackageInfo


class CppHeaderCollectionWriter:
    """
    Class to manage the generation of the header collection file.

    The header collection file includes all the headers to be parsed by CastXML.
    It also contains explicit template instantiations and their corresponding
    typedefs (e.g. typedef Foo<2,2> Foo_2_2) for all classes that are to be
    automatically wrapped.

    Attributes
    ----------
        package_info : PackageInfo
            The package information
        wrapper_root : str
            The output directory for the generated wrapper code
        hpp_collection_filepath : str
            The path to save the header collection file to
        hpp_collection_string : str
            The output string that gets written to the header collection file
        class_dict : Dict[str, CppClassInfo]
            A dictionary of all class info objects
        free_func_dict : Dict[str, CppFreeFunctionInfo]
            A dictionary of all free function info objects
    """

    def __init__(
        self,
        package_info: PackageInfo,
        wrapper_root: str,
        hpp_collection_filepath: str,
    ):

        self.package_info: PackageInfo = package_info
        self.wrapper_root: str = wrapper_root
        self.hpp_collection_filepath: str = hpp_collection_filepath
        self.hpp_collection_string: str = ""

        # For convenience, collect all class and free function info into dicts keyed by name
        self.class_dict: Dict[str, CppClassInfo] = {}
        self.free_func_dict: Dict[str, CppFreeFunctionInfo] = {}

        for module_info in self.package_info.module_info_collection:
            for class_info in module_info.class_info_collection:
                self.class_dict[class_info.name] = class_info

            for free_function_info in module_info.free_function_info_collection:
                self.free_func_dict[free_function_info.name] = free_function_info

    def should_include_all(self) -> bool:
        """
        Return whether all source files in the module source locations should be included.

        Returns
        -------
        bool
        """
        # True if any module uses all classes or all free functions
        for module_info in self.package_info.module_info_collection:
            if module_info.use_all_classes or module_info.use_all_free_functions:
                return True
        return False

    def write(self) -> None:
        """Generate the header file output string and write it to file."""
        # Add the top prefix text
        self.hpp_collection_string += self.package_info.prefix_text + "\n"

        # Add opening header guard
        self.hpp_collection_string += f"#ifndef {self.package_info.name}_HEADERS_HPP_\n"
        self.hpp_collection_string += f"#define {self.package_info.name}_HEADERS_HPP_\n"

        self.hpp_collection_string += "\n// Includes\n"

        included_files = set()  # Keep track of included files to avoid duplicates

        if self.should_include_all():
            # Include all the headers
            for hpp_filepath in self.package_info.source_hpp_files:
                hpp_filename = os.path.basename(hpp_filepath)

                if hpp_filename not in included_files:
                    self.hpp_collection_string += f'#include "{hpp_filename}"\n'
                    included_files.add(hpp_filename)

        else:
            # Include specific headers needed by classes
            for module_info in self.package_info.module_info_collection:
                for class_info in module_info.class_info_collection:
                    # Skip excluded classes
                    if class_info.excluded:
                        continue

                    hpp_filename = None

                    if class_info.source_file:
                        hpp_filename = class_info.source_file

                    elif class_info.source_file_full_path:
                        hpp_filename = os.path.basename(
                            class_info.source_file_full_path
                        )

                    if hpp_filename and hpp_filename not in included_files:
                        self.hpp_collection_string += f'#include "{hpp_filename}"\n'
                        included_files.add(hpp_filename)

                # Include specific headers needed by free functions
                for free_function_info in module_info.free_function_info_collection:
                    if free_function_info.source_file_full_path:
                        hpp_filename = os.path.basename(
                            free_function_info.source_file_full_path
                        )

                        if hpp_filename not in included_files:
                            self.hpp_collection_string += f'#include "{hpp_filename}"\n'
                            included_files.add(hpp_filename)

        # Add the template instantiations e.g. `template class Foo<2,2>;`
        # and typdefs e.g. `typedef Foo<2,2> Foo_2_2;`
        template_instantiations = ""
        template_typedefs = ""

        for module_info in self.package_info.module_info_collection:
            for class_info in module_info.class_info_collection:
                # Skip excluded classes
                if class_info.excluded:
                    continue

                # Skip untemplated classes
                if not class_info.template_arg_lists:
                    continue

                # C++ class names eg. ["Foo<2,2>", "Foo<3,3>"]
                cpp_names = [name.strip() for name in class_info.cpp_names]

                # Python class names eg. ["Foo_2_2", "Foo_3_3"]
                py_names = [name.strip() for name in class_info.py_names]

                for cpp_name, py_name in zip(cpp_names, py_names):
                    template_instantiations += f"template class {cpp_name};\n"
                    template_typedefs += f"    typedef {cpp_name} {py_name};\n"

        self.hpp_collection_string += "\n// Instantiate Template Classes\n"
        self.hpp_collection_string += template_instantiations

        self.hpp_collection_string += "\n// Typedefs for nicer naming\n"
        self.hpp_collection_string += "namespace cppwg\n{\n"
        self.hpp_collection_string += template_typedefs
        self.hpp_collection_string += "} // namespace cppwg\n"

        # Add closing header guard
        self.hpp_collection_string += (
            f"\n#endif // {self.package_info.name}_HEADERS_HPP_\n"
        )

        # Write the header collection string to file
        with open(self.hpp_collection_filepath, "w") as hpp_file:
            hpp_file.write(self.hpp_collection_string)
