"""C++ type information structure."""

from typing import Any, Dict, List, Optional

from cppwg.info.base_info import BaseInfo


class CppTypeInfo(BaseInfo):
    """
    An information structure for C++ types including classes, free functions etc.

    Attributes
    ----------
    decls : pygccxml.declarations.declaration_t
        The pygccxml declarations associated with this type, one per template arg if templated
    module_info : ModuleInfo
        The module info parent object associated with this type
    name_override : str
        The name override specified in config e.g. "CustomFoo" -> "Foo"
    source_file : str
        The source file containing the type
    source_file_full_path : str
        The full path to the source file containing the type
    template_arg_lists : List[List[Any]]
        List of template replacement arguments e.g. [[2, 2], [3, 3]]
    template_params : List[str]
        List of template parameters e.g. ["DIM_A", "DIM_B"]
    template_signature : str
        The template signature of the type e.g. "<unsigned DIM_A, unsigned DIM_B = DIM_A>"
    """

    def __init__(self, name: str, type_config: Optional[Dict[str, Any]] = None):

        super().__init__(name)

        self.module_info: Optional["ModuleInfo"] = None  # noqa: F821

        self.name_override: Optional[str] = None

        self.source_file: str = ""
        self.source_file_full_path: str = ""

        self.template_arg_lists: Optional[List[List[Any]]] = None
        self.template_params: Optional[List[str]] = None
        self.template_signature: Optional[str] = None

        self.decls: Optional[List["declaration_t"]] = None  # noqa: F821

        if type_config:
            for key, value in type_config.items():
                setattr(self, key, value)

    def set_module(self, module_info: "ModuleInfo") -> None:  # noqa: F821
        """
        Set the associated module info object.
        """
        self.module_info = module_info
