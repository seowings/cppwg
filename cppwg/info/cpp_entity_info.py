"""C++ entity information structure."""

from typing import Any, Dict, List, Optional

from cppwg.info.base_info import BaseInfo


class CppEntityInfo(BaseInfo):
    """
    An information structure for C++ entities including classes, free functions etc.

    Attributes
    ----------
    name_override : str
        The name override specified in config e.g. "CustomFoo" -> "Foo"
    source_file : str
        The source file containing the entity
    source_file_path : str
        The full path to the source file containing the entity

    module_info : ModuleInfo
        The module info object that this entity belongs to

    decls : pygccxml.declarations.declaration_t
        The pygccxml declarations associated with this entity, one per template arg if templated
    template_arg_lists : List[List[Any]]
        List of template replacement arguments e.g. [[2, 2], [3, 3]]
    template_params : List[str]
        List of template parameters e.g. ["DIM_A", "DIM_B"]
    template_signature : str
        The template signature of the entity e.g. "<unsigned DIM_A, unsigned DIM_B = DIM_A>"
    """

    def __init__(self, name: str, entity_config: Optional[Dict[str, Any]] = None):
        super().__init__(name, entity_config)

        self.name_override: str = ""
        self.source_file: str = ""
        self.source_file_path: str = ""

        self.module_info: Optional["ModuleInfo"] = None  # noqa: F821

        self.decls: List["declaration_t"] = []  # noqa: F821
        self.template_arg_lists: List[List[Any]] = []
        self.template_params: List[str] = []
        self.template_signature: str = ""

        if entity_config:
            for key in ["name_override", "source_file", "source_file_path"]:
                if key in entity_config:
                    setattr(self, key, entity_config[key])

    @property
    def parent(self) -> "ModuleInfo":  # noqa: F821
        """
        Returns the module info object that holds this entity.
        """
        return self.module_info

    @parent.setter
    def parent(self, module_info: "ModuleInfo") -> None:  # noqa: F821
        """
        Set the module info object that holds this entity.
        """
        self.module_info = module_info
