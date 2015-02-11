class node:
    def __init__(self):
        self.value = ""
        self.type = ""
        self.parent = None
        self.children = [] # stack with all the nocdes
    def appendchild(self):
        self.children.append(node())
        self.children[self.countchild()-1].parent = self
    def getchild(self,nr):
        if len(self.children) < nr:
            return None
        else:
            return self.children[nr]
    def countchild(self):
        return len(self.children)
    def setval(self,val):
        self.value = val
    def setname(self,name):
        self.name = name
    def getchildren(self):
        return self.children
    
test = node()
test.appendchild()
test.appendchild()
my = test.getchild(0)
my.setval("ADD")
print(my.value)
test.appendchild()
print(test.countchild())