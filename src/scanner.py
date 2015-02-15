import token
from curses.ascii import isalpha
# Helper functions #
def iswhitespace(c):
    return c in ['\n','\t',' ']
def isnum(d):
    return d in ["1","2","3","4","5","6","7","8","9","0"]
# Implements a scanner
# Returns the next token

# ISSUE Scanner error with <=
class Scanner:
    def __init__(self):
        print("Scanning source file")
        self.char = 0
        self.line = 1
        self.eofp = False
        
    def scan(self,fname):
        self.fname = fname
        self.file = open(fname,"r")
        self.character = self.get()
    def gettoken(self):
        self.token = self.gettoken_intern()
        return self.token
    def getCurrent(self):
        return self.token
    def gettoken_intern(self):
        ''' @returns next token '''
        while iswhitespace(self.character):
            self.character = self.get()
        # Skipped whitespaces
        ct = token.token()
        if self.character == "EOF":
            self.eofp = True
            ct.construct("EOF",self.line,self.char,"EOF")
            return ct
        if self.character == "+":
            # construct the token
            self.character = self.get()
            ct.construct("PLUS",self.line,self.char,"+")
            return ct
        
        if self.character == "-":
            self.character = self.get()
            ct.construct("MINUS",self.line,self.char,"-")
            return ct
        if self.character == "*":
            self.character = self.get()
            ct.construct("STAR",self.line,self.char,"*")
            return ct
        if self.character == ":":
            self.character = self.get()
            if self.character == "=":
                ct.construct("COLON_EQUALS",self.line,self.char,":=")
                self.character = self.get()
                return ct
            ct.construct("COLON",self.line,self.char,":")
            return ct
        if self.character == ".":
            self.character = self.get()
            if self.character == ".":
                ct.construct("DOT_DOT",self.line,self.char,"..") 
                return ct
            ct.construct("DOT",self.line,self.char,".")
            return ct
        
        if self.character == ",":
            self.character = self.get()
            ct.construct("COMMA",self.line,self.char,",")
            return ct
        if self.character == ";":
            self.character = self.get()
            ct.construct("SEMICOLON",self.line,self.char,";")
            return ct
        
        if self.character == "=":
            self.character = self.get()
            ct.construct("EQUALS",self.line,self.char,"=")
            return ct
        
        if self.character == "<":
            self.character = self.get()
            if self.character == ">":
                self.character = self.get()
                ct.construct("NOT_EQUALS",self.line,self.char,"<>")
                return ct
            if self.character == "=":
                self.character = self.get()
                ct.construct("LESS_EQUALS",self.line,self.char,"<=")
                return ct
            ct.construct("LESS_THAN",self.line,self.char,"<")
            return ct
        
        if self.character == ">":
            self.charcter = self.get()
            if self.character == "=":
                self.character = self.get()
                ct.construct("GREATER_EQUALS",self.line,self.char,">=")
                return ct
            ct.construct("GREATER_THAN",self.line,self.char,">")
            return ct
        
        if self.character == "(":
            self.character = self.get()
            ct.construct("LPAREN",self.line,self.char,"(")
            return ct
        
        if self.character == ")":
            self.character = self.get()
            ct.construct("RPAREN",self.line,self.char,")")
            return ct
        
        if self.character == "[":
            self.character = self.get()
            ct.construct("RBRACKET",self.line,self.char,"[")
            return ct
        
        if self.character == "]":
            self.character = self.get()
            ct.construct("LBRACKET",self.line,self.char,"]")
            return ct
        if self.character == "{":
            self.character = self.get()
            ct.construct("RBRACE",self.line,self.char,"{")
            return ct
        
        if self.character == "}":
            self.character = self.get()
            ct.construct("LBRACE",self.line,self.char,"}")
            return ct
                
        if self.character == "^":
            self.character = self.get()
            ct.construct("UP_ARROW",self.line,self.char,"^")
            return ct
        if self.character == "/":
            self.character = self.get()
            ct.construct("SLASH",self.line,self.char,"/")
            return ct
        if self.character == "'":
            self.character = self.get()
            string = ""
            while self.character != "'":
                string += self.character
                self.character = self.file.read(1)
                if not self.character:
                    self.mark("Unterminated String")
                    return None
            self.character = self.get()
            #self.character = self.get()
            ct.construct("STRING",self.line,self.char,string)
            return ct    
        if isalpha(self.character):
            ident = ""
            while isalpha(self.character):
                ident += self.character
                self.character = self.get()
            # check if identifier is a reserved word #
            
            ct.construct("IDENT",self.line,self.char,ident,ident)
            if ident.lower() in  [x.lower() for x in ["AND","ARRAY","BEGIN","CASE","CONST","DIV","DO","DOWNTO","ELSE","END","FILE","FOR","FUNCTION","GOTO","IF","IN","LABEL","MOD","NIL","NOT","OF","OR","PACKED","PROCEDURE","PROGRAM","RECORD","REPEAT","SET","THEN","TO","TYPE","UNTIL","VAR","WHILE","WITH"] ]:
                ct.construct(ident.upper(),self.line,self.char,ident)
            return ct
        if self.character == "%":
            pass # BINARY NUMBER #
        if isnum(self.character):
            digit = ""
            while isnum(self.character) or self.character == ".":
                digit += self.character
                self.character = self.get()
            if '.' in digit:
                ct.construct("REAL",self.line,self.char,digit,digit)
                return ct
            ct.construct("INT",self.line,self.char,digit,digit)
            return ct
        self.mark("Unknown token %c"%(self.character))
    def mark(self,err,warninglevel=2):
        if warninglevel == 2:
            print("%s %.3i::%.2i Error: %s"%(self.fname,self.line,self.char,err))
            raise "Parser Error"
        if warninglevel == 1:
            print("%s %.3i::%.2i Warning: %s"%(self.fname,self.line,self.char,err))
        if warninglevel == 0:
            print("%s %.3i::%.2i Hint: %s"%(self.fname,self.line,self.char,err))
    def get(self,ws = False):
        # Method for getting internally #
        character = self.file.read(1)
        if not character:
            return "EOF"
        if character == '\n':
            self.line += 1
            self.char = 0
            return character
        if character == '\t':
            return character
        if character == '{':
            if ws:
                return character
            else:
                self.skipcomment()
                return self.get()
        self.char += 1
        return character
    def skipcomment(self):
        ch = self.get()
        while ch != "}":
            ch = self.get()

