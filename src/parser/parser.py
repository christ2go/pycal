import scanner
import sys
from tree import treeprint
sys.path.append("../tree/")
import node
class parser(object):
    def __init__(self, fname):
        self.scanner = scanner.Scanner()
        self.scanner.scan(fname)
        self.tree = node.node()
    def printtoken(self):
        while True:
            token = self.scanner.gettoken()
            if token.tokentype != "EOF":
                print(token)
            else:
                return
            
    def parse(self):
        self.token = self.scanner.gettoken()
        if(self.token.tokentype == "BEGIN"):
            pnode = self.parseStatement()
            self.tree = pnode
        else:
            self.scanner.mark("EXSPECTED BEGIN")
        if self.token.tokentype != "DOT":
            self.scanner.mark("Exspected DOT got %s"%(self.token.tokentype))
    def parseStatement(self):
        stmt = None
        if self.token.tokentype == "BEGIN":
            stmt = self.parseCompound()
            return stmt
        elif self.token.tokentype == "IDENT":
            stmt = self.parseAssign()
        elif self.token.tokentype == "REPEAT":
            stmt = self.parseRepeatStatement()
        elif self.token.tokentype == "WHILE":
            stmt = self.parseWhileStatement()
        elif self.token.tokentype == "IF":
            stmt = self.parseIfStatement()
        elif self.token.tokentype == "CASE":
            pass
        else:
            stmt = node.node("NO_OP")
        return stmt
    def parseStatementList(self, token, parent, term, err):
        while self.token.tokentype != "EOF" and self.token.tokentype != term:
            statementnode = self.parseStatement()
            parent.appendChild(statementnode)
            if self.token.tokentype == "SEMICOLON":
                self.token = self.scanner.gettoken()
            elif self.token.tokentype == "IDENT":
                self.scanner.mark("Missing Semicolon")
            elif self.token.tokentype in ["FOR","WHILE","IF","REPEAT"]:
                self.scanner.mark("Missing ;")
            elif self.token.tokentype != term:
                self.scanner.mark("=>Missing Terminator - exspected %s and got %s" % (term, self.token.tokentype))
                self.token = self.scanner.gettoken()
        if self.token.tokentype == term:
            self.token = self.scanner.gettoken()
            return
        else:
            self.scanner.mark("Missing Terminator - exspected %s and got %s" % (term, self.token.tokentype))
            
    def parseCompound(self):
        self.token = self.scanner.gettoken()
        compnode = node.node("COMPOUND")
        self.parseStatementList(self.token, compnode, "END", "MISSING END")
        return compnode
    def parseAssign(self):
        assignnode = node.node("ASSIGN")
        targetname = self.token.getText()
        # Symbol table
        varnode = node.node("VARIABLE")
        varnode.set("ID", targetname)
        assignnode.appendChild(varnode)
        self.token = self.scanner.gettoken()
        if self.token.tokentype == "COLON_EQUALS":
            self.token = self.scanner.gettoken()  # consume it
        else:
            self.scanner.mark("Exspected := , not " + self.token.text)
        assignnode.appendChild(self.parseExpression())
        return assignnode
    def parseExpression(self):
        rootnode = self.parseSimpleExpression()
        tokentype = self.token.tokentype
        if tokentype in ["EQUALS", "NOT_EQUALS", "LESS_THAN", "LESS_EQUALS", "GREATER_THAN", "GREATER_EQUALS"]:
            if tokentype == "EQUALS":
                nodetype = "EQ"
            if tokentype == "NOT_EQUALS":
                nodetype = "NE"
            if tokentype == "LESS_THAN":
                nodetype = "LT"
            if tokentype == "LESS_EQUALS":
                nodetype = "LE"
            if tokentype == "GREATER_THAN":
                nodetype = "GT"
            if tokentype == "GREATER_EQUALS":
                nodetype = "GE"
            opNode = node.node(nodetype)
            self.token = self.scanner.gettoken()
            opNode.appendChild(self.parseSimpleExpression())
            rootnode = opNode
        return rootnode
    
    def parseSimpleExpression(self):
        signtype = None
        tokentype = self.token.tokentype
        
        if tokentype == "PLUS" or tokentype == "MINUS":
            signtype = tokentype
            self.token = self.scanner.gettoken() 
        rootnode = self.parseTerm()
        
        if signtype == "MINUS":
            negnode = node.node("NEGATE")
            negnode.appendChild(rootnode)
            rootnode = negnode
        add_ops = {
                   "PLUS":"ADD",
                   "MINUS":"SUBTRACT"
                }
        tokentype = self.token.tokentype
        while (tokentype) in add_ops:
            nodetype = add_ops[tokentype]
            opNode = node.node(nodetype)
            opNode.appendChild(rootnode)
            self.token = self.scanner.gettoken()
            opNode.appendChild(self.parseTerm())
            rootnode = opNode
            self.token = self.scanner.getCurrent()
            tokentype = self.token.tokentype
        return rootnode
    def parseTerm(self):
        mulops = {
                  "STAR": "MULTIPLY",
                  "SLASH": "FLOAT_DIVIDE",
                  "DIV": "INTEGER_DIVIDE",
                  "MOD": "MOD",
                  "AND": "AND"
                }
        rootnode = self.parseFactor()
        
        while self.token.tokentype in mulops:
            nodetype = mulops[self.token.tokentype]
            opnode = node.node(nodetype)
            opnode.appendChild(rootnode)
            self.token = self.scanner.gettoken()
            opnode.appendChild(self.parseFactor())
            rootnode = opnode
        return rootnode
    
    def parseFactor(self):
        tokentype = self.token.tokentype
        rootnode = None
        
        if tokentype == "IDENT":
            name = self.token.text.lower()
            # TODO Check symbol table for entries
            rootnode = node.node("VARIABLE")
            rootnode.set("ID",name)
            # Append line number - maybe (?)
            self.token = self.scanner.gettoken()
        elif tokentype == "INT":
            rootnode = node.node("INTEGER_CONSTANT")
            rootnode.set("VALUE",self.token.value)
            self.token = self.scanner.gettoken()
            tokentype = self.token.tokentype
        elif tokentype == "STRING":
            rootnode = node.node("STRING_CONSTANT")
            rootnode.set("VALUE",self.token.text)
            self.token = self.scanner.gettoken()
            tokentype = self.token.tokentype
        elif tokentype == "REAL":
            rootnode = node.node("REAL_CONSTANT")
            rootnode.set("VALUE",self.token.value)
            self.token = self.scanner.gettoken()
            tokentype = self.token.tokentype
        elif tokentype == "NOT":
            self.token = self.scanner.gettoken()
            rootnode = node.node("NOT")
            rootnode.appendChild(self.parseFactor())
            
        elif tokentype == "LPAREN":
            self.token = self.scanner.gettoken()
            rootnode = self.parseExpression()
            if self.token.tokentype != "RPAREN":
                self.scanner.mark("Missing )")
            self.token = self.scanner.gettoken()
        return rootnode
    def parseRepeatStatement(self):
        self.token = self.scanner.gettoken()
        # Consume the REPEAT
        loopnode = node.node("LOOP")
        testnode = node.node("TEST")
        self.parseStatementList(self.token, loopnode, "UNTIL", "Missing until")
        testnode.appendChild(self.parseExpression())
        loopnode.appendChild(testnode)
        return loopnode
    def parseIfStatement(self):
        ifNode = node.node("IF")
        # TODO SYNCHRONIZE
        self.token = self.scanner.gettoken()
        ifNode.appendChild(self.parseExpression())
        if self.token.tokentype == "THEN":
            self.token = self.scanner.gettoken()
        else:
            self.scanner.mark("Missing THEN in IFELSE not %s"%(self.token.text))
        ifstmt = self.parseStatement()
        ifNode.appendChild(ifstmt)
        self.token = self.scanner.gettoken()
        if self.token.tokentype == "ELSE":
            self.token = self.scanner.gettoken()
            ifNode.appendChild(self.parseStatement())
        return ifNode
    def parseWhileStatement(self):
        self.token = self.scanner.gettoken() # Consume the WHILE
        notnode = node.node("NOT") # Node for test
        testnode = node.node("TEST")
        loopnode = node.node("LOOP")
        notnode.appendChild(self.parseExpression())  # Append <test> to notnode
        testnode.appendChild(notnode)
        loopnode.appendChild(testnode)
        # EXSPECT DO STATEMENT
        if self.token.tokentype != "DO":
            self.scanner.mark("Missing DO in WHILE, (not \"%s\")"%(self.token.tokentype))
        else:
            self.token = self.scanner.gettoken()
        loopnode.appendChild(self.parseStatement())
        return loopnode
    def CaseStatement(self):
        pass
    def ForStatement(self):
        pass
    
test = parser("../examples/whiletest.PAS")
test.parse()
x = treeprint.treeprinter(test.tree)
x.printt()