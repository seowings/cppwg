import os
import logging

from pygccxml.declarations.class_declaration import class_t
from pygccxml.declarations.namespace import namespace_t

from cppwg.input.module_info import ModuleInfo

from cppwg.writers.free_function_writer import CppFreeFunctionWrapperWriter
from cppwg.writers.class_writer import CppClassWrapperWriter

from cppwg.utils.constants import CPPWG_HEADER_COLLECTION_FILENAME


class CppModuleWrapperWriter:
    """
    This class automatically generates Python bindings using a rule based approach

    Attributes
    ----------
    source_ns : namespace_t
        The pygccxml namespace containing declarations from the source code
    module_info : ModuleInfo
        The module information to generate Python bindings for
    wrapper_templates : dict[str, str]
        String templates with placeholders for generating wrapper code
    wrapper_root : str
        The output directory for the generated wrapper code
    package_license : str
        The license to include in the generated wrapper code
    """

    def __init__(
        self,
        source_ns: namespace_t,
        module_info: ModuleInfo,
        wrapper_templates: dict[str, str],
        wrapper_root: str,
        package_license: str = "",
    ):
        self.source_ns: namespace_t = source_ns
        self.module_info: ModuleInfo = module_info
        self.wrapper_templates: dict[str, str] = wrapper_templates
        self.wrapper_root: str = wrapper_root
        self.package_license: str = (
            package_license  # TODO: use this in the generated wrappers
        )

        # For convenience, create a list of all full class names in the module
        # e.g. ['Foo', 'Bar<2>', 'Bar<3>']
        self.exposed_class_full_names: list[str] = []

        for class_info in self.module_info.class_info_collection:
            self.exposed_class_full_names.extend(class_info.get_full_names())

    def write_module_wrapper(self) -> None:
        """
        Write the main cpp file for the module
        """

        # Format module name as _packagename_modulename
        module_name = self.module_info.name
        full_module_name = "_" + self.module_info.package_info.name + "_" + module_name

        # Add top level includes
        cpp_string = "#include <pybind11/pybind11.h>\n"

        if self.module_info.package_info.common_include_file:
            cpp_string += f'#include "{CPPWG_HEADER_COLLECTION_FILENAME}"\n'

        # Add outputs from running custom generator code
        if self.module_info.custom_generator:
            cpp_string += self.module_info.custom_generator.get_module_pre_code()

        # Add includes for class wrappers in the module
        for class_info in self.module_info.class_info_collection:
            for short_name in class_info.get_short_names():
                # Example: #include "Foo2_2.cppwg.hpp"
                cpp_string += f'#include "{short_name}.cppwg.hpp"\n'

        # Create the module
        cpp_string += "\nnamespace py = pybind11;\n\n"
        cpp_string += "PYBIND11_MODULE({full_module_name}, m)\n{\n"

        # Add free functions
        for free_function_info in self.module_info.free_function_info_collection:
            function_writer = CppFreeFunctionWrapperWriter(
                free_function_info, self.wrapper_templates
            )
            cpp_string = function_writer.add_self(cpp_string)

        # Add viable classes
        for class_info in self.module_info.class_info_collection:
            for short_name in class_info.get_short_names():
                cpp_string += "    register_" + short_name + "_class(m);\n"

        # Add any custom code
        if self.module_info.custom_generator is not None:
            cpp_string += self.module_info.custom_generator.get_module_code()

        output_dir = self.wrapper_root + "/" + self.module_info.name + "/"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        main_cpp_file = open(output_dir + self.module_info.name + ".main.cpp", "w")
        main_cpp_file.write(cpp_string + "}\n")
        main_cpp_file.close()

    def write_class_wrappers(self) -> None:
        """
        Write wrappers for classes in the module
        """
        logger = logging.getLogger()

        for class_info in self.module_info.class_info_collection:
            logger.info(f"Generating wrapper for class {class_info.name}")

            class_writer = CppClassWrapperWriter(
                class_info, self.wrapper_templates, self.exposed_class_full_names
            )

            for full_name in class_info.get_full_names():
                name: str = full_name.replace(" ", "")

                class_decl: class_t = self.source_ns.class_(name)
                class_writer.class_decls.append(class_decl)
            class_writer.write(os.path.join(self.wrapper_root, self.module_info.name))

    def write(self) -> None:
        """
        Main method for writing the module
        """
        logger = logging.getLogger()

        logger.info(f"Generating wrappers for module {self.module_info.name}")

        self.write_module_wrapper()
        self.write_class_wrappers()
