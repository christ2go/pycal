import treeprint
def traverse(tree,ident = 1):
    me = treeprint.treeprinter(tree)
    me.printt()

class node:
    def __init__(self,name = ""):
        self.parent = None
        self.children = [] # stack with all the nocdes
        self.name = name
        self.attr = {}
    def appendchild(self,name=None):
        self.children.append(node())
        self.children[self.countchild()-1].parent = self
        if name != None:
            self.children[self.countchild()-1].name = name
        return self.children[-1]
    def appendChild(self,child):
        self.children.append(child)
    def getchild(self,nr):
        if len(self.children) < nr:
            return None
        else:
            return self.children[nr]
    def countchild(self):
        return len(self.children)
    def setname(self,name):
        self.name = name
    def getchildren(self):
        return self.children
    def appendchilds(self,num):
        for i in range(0,num):
            self.appendchild()
    def set(self,name,val):
        self.attr[name] = val
    def get(self,name):
        return self.attr[name]
    
"""       
test = node("COMPOUND")
x = test.appendchild("ASSIGN")
y = x.appendchild("VARIABLE")
y.set("name","alpha")
z = x.appendchild("NEGATE")
a = z.appendchild("INTEGER CONSTANT")
a.set("value",58)

# Middle side
x = test.appendchild("ASSIGN")
r = x.appendchild("VARIABLE")
z.set("name","beta")
z = x.appendchild("INTEGER CONSTANT")
z.set("value","99")

x = test.appendchild("ASSIGN")
z = x.appendchild("VARIABLE")
z.set("name","result")
z = x.appendchild("ADD")
r = x
a = z.appendchild("ADD")
b = a.appendchild("VARIABLE")
b.set("name","alpha")

b = a.appendchild("FLOAT DIVIDE")
c = b.appendchild("INTEGER CONSTANT")
c.set("value","3")
c = b.appendchild("SUBTRACT")
d = c.appendchild("VARIABLE")
d.set("name","beta")
d = c.appendchild("VARIABLE")
d.set("name","gamma")

d = r.appendchild("INTEGER CONSTANT")
d.set("value","5")

traverse(test)
"""
