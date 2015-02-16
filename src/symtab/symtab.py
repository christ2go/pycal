
class symtab:
    def __init__(self):
        self.entries = [];
    def getNestingLevel(self):
        pass
    def enter(self):
        pass
    def lookup(self,name):
        for element in self.entries:
            if element.name == name:
                return element
        return None
    