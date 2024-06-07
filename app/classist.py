class ChildDoesntExist(Exception):
    pass

class crd_object:
    def __init__(self, name:str, indent:int, description:str="", types:str="", classes:list=[], *args) -> None:
        self.name = name
        self.info = args
        self.description = description
        self.types = types
        self.classes = classes
        self.indent = indent
    
    def __repr__(self) -> str:
        return f"{self.name}:({self.types}{self.description}) {self.indent}"

    def add_description(self, description):
        self.description = description
    
    def add_types(self, types):
        self.types = types

    def add_info(self, info):
        self.info = info