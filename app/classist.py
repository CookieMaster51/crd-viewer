class ChildDoesntExist(Exception):
    pass

class crd_object:
    def __init__(self, childs:list, name:str, description:str="", types:str="", *args) -> None:
        self.childs = childs
        self.name = name
        self.info = args
        self.description = description
        self.types = types
    
    def __repr__(self) -> str:
        return f"{self.name} {str(self.childs)}"
    
    def add_child(self, other):
        self.childs.append(other)

    def add_description(self, description):
        self.description = description
    
    def add_types(self, types):
        self.types = types

    def add_info(self, info):
        self.info = info

    def remove_child(self, to_remove):
        try:
            self.childs.remove(to_remove)
        except ValueError:
            raise ChildDoesntExist