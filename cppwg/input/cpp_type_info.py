from typing import Any, Optional

from cppwg.input.base_info import BaseInfo

from pygccxml.declarations import declaration_t


class CppTypeInfo(BaseInfo):
    """
    This class holds informatioin for C++ variables and functions

    Attributes
    ----------
    module_info : ModuleInfo
        The module info parent object associated with this variable or function
    source_file : str
        The source file containing the variable or function
    source_file_full_path : str
        The full path to the source file containing the variable or function
    name_override : str
        The name override specified in config e.g. "SharedPottsMeshGenerator" -> "PottsMeshGenerator"
    decl : declaration_t
        The pygccxml declaration associated with this variable or function
    """

    def __init__(self, name: str, type_config: Optional[list[str, Any]] = None):

        super(CppTypeInfo, self).__init__(name)

        self.module_info = None  # : ModuleInfo
        self.source_file_full_path: str = None
        self.source_file: str = None
        self.name_override: str = None
        self.template_args = None
        self.decl: declaration_t = None

        if type_config is not None:
            for key, value in type_config.items():
                setattr(self, key, value)

    def get_short_names(self):
        """
        Return the name of the class as it will appear on the Python side. This
        collapses template arguements, separating them by underscores and removes
        special characters. The return type is a list, as a class can have multiple
        names if it is templated.
        """

        if self.template_args is None:
            if self.name_override is None:
                return [self.name]
            else:
                return [self.name_override]

        names = []
        for eachTemplateArg in self.template_args:
            template_string = ""
            for idx, eachTemplateEntry in enumerate(eachTemplateArg):

                # Do standard translations
                current_name = str(eachTemplateEntry)
                for eachReplacementString in self.name_replacements.keys():
                    replacement = self.name_replacements[eachReplacementString]
                    current_name = current_name.replace(
                        eachReplacementString, replacement
                    )

                table = current_name.maketrans(dict.fromkeys("<>:,"))
                cleaned_entry = current_name.translate(table)
                cleaned_entry = cleaned_entry.replace(" ", "")
                if len(cleaned_entry) > 1:
                    first_letter = cleaned_entry[0].capitalize()
                    cleaned_entry = first_letter + cleaned_entry[1:]
                template_string += str(cleaned_entry)
                if idx != len(eachTemplateArg) - 1:
                    template_string += "_"

            current_name = self.name
            if self.name_override is not None:
                current_name = self.name_override

            # Do standard translations
            for eachReplacementString in self.name_replacements.keys():
                replacement = self.name_replacements[eachReplacementString]
                current_name = current_name.replace(eachReplacementString, replacement)

            # Strip templates and scopes
            table = current_name.maketrans(dict.fromkeys("<>:,"))
            cleaned_name = current_name.translate(table)
            cleaned_name = cleaned_name.replace(" ", "")
            if len(cleaned_name) > 1:
                cleaned_name = cleaned_name[0].capitalize() + cleaned_name[1:]
            names.append(cleaned_name + template_string)
        return names

    def get_full_names(self):
        """
        Return the name (declaration) of the class as it appears on the C++ side.
        The return type is a list, as a class can have multiple
        names (declarations) if it is templated.
        """

        if self.template_args is None:
            return [self.name]

        names = []
        for eachTemplateArg in self.template_args:
            template_string = "<"
            for idx, eachTemplateEntry in enumerate(eachTemplateArg):
                template_string += str(eachTemplateEntry)
                if idx == len(eachTemplateArg) - 1:
                    template_string += " >"
                else:
                    template_string += ","
            names.append(self.name + template_string)
        return names

    def needs_header_file_instantiation(self):
        """
        Does this class need to be instantiated in the header file
        """

        return (
            (self.template_args is not None)
            and (not self.include_file_only)
            and (self.needs_instantiation)
        )

    def needs_header_file_typdef(self):
        """
        Does this type need to be typdef'd with a nicer name in the header
        file. All template classes need this.
        """

        return (self.template_args is not None) and (not self.include_file_only)

    def needs_auto_wrapper_generation(self):
        """
        Does this class need a wrapper to be autogenerated.
        """

        return not self.include_file_only
