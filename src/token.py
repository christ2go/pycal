# Implements a token class

class token:
    def __init__(self):
        self.tokentype = None
        self.text = None
        self.value = None
        self.lineNum = None
        self.position = None
    
    def setType(self,tokentype):
        self.type = tokentype
    def setText(self,text):
        self.text = text
    def setValue(self,value):
        self.value = value;
    def setLinenum(self,line):
        self.lineNum = line
    def setPosition(self,position):
        self.position = position 
    def getText(self):
        return self.text
    def construct(self,ttype,line,pos,text,value = None):
        self.tokentype =  ttype
        self.lineNum = line
        self.position = pos
        self.text = text
        self.value = value
    def __str__(self):
        if self.value == None:
            return("%-15s line=%.3i, pos=%.3i, text=%s"%(self.tokentype,self.lineNum,self.position,self.text))
        else:
            return("%-15s line=%.3i, pos=%.3i, text=%s\n%-15s value=%s"%(self.tokentype,self.lineNum,self.position,self.text,"",self.value))
