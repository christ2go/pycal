def write(x):
    print(x,end="")
class treeprinter:
    """
        Prints an abstract syntax tree
        as a XML-Document 
        
        tree has to be instaneceof node
        (tree is the AST to be printed)
    """
    def __init__(self,tree):
        self.tree = tree
    def printt(self):
        if not self.tree:
            raise "Tree Exception - Tree not initialized"
            return False
        self.recprint(self.tree)
    def writeattr(self,node):
        for key in node.attr:
            write(" "+key+"="+str(node.attr[key]))
            
    def recprint(self,node,ident=0):
        write("   "*ident)
        write("<")
        write(node.name.replace(" ","_"))
        write("")
        self.writeattr(node)
        if len(node.children) != 0:
            write(">")
            write("\n")
            
            for item in node.children:
                self.recprint(item,ident+1)
           # write("\n")
            write("   "*ident)
            write("</"+node.name.replace(" ","_")+">")
            write("\n")
        else:
            write(" />"+"\n")
