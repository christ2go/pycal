import scanner
import sys
sys.path.append("../tree/")
import node
class parser(object):
    def __init__(self,fname):
        self.scanner = scanner.Scanner()
        self.scanner.scan(fname)
        self.tree = node.node()
    def parse(self):
        self.token = self.scanner.gettoken()
        if(self.token.tokentype == "BEGIN"):
            pnode = self.parseStatement()
            self.tree = pnode
        else:
            self.scanner.mark("EXSPECTED BEGIN")
        if self.token.tokentype != "DOT":
            self.scanner.mark("Exspected DOT")
    def parseStatement(self):
        if self.token.tokentype == "BEGIN":
            stmt = self.parseCompound()
            return stmt
        elif self.token.tokentype == "IDENTIFIER":
            statementnode = self.parseAssign()
        else:
            stmt = node.node("NO_OP")
            return stmt
    def parseStatementList(self,token,parent,term,err):
        while self.token.tokentype != "EOF":
            statementnode = self.parseStatement()
            parent.appendChild(statementnode)
            if self.token.tokentype == "SEMICOLON":
                self.token = self.scanner.gettoken()
            elif self.token.tokentype == "IDENT":
                self.scanner.mark("Missing Semicolon")
            elif self.token.tokentype != term:
                self.scanner.mark("Unexspected Token ")
                self.token = self.scanner.gettoken()
            if self.token.tokentype == term:
                self.token = self.scanner.gettoken()
            else:
                self.scanner.mark("Missing Terminator")
    def parseCompound(self):
        self.token = self.scanner.gettoken()
        compnode = node.node()
        self.parseStatementList(self.token, compnode, "END", "MISSING END")
    def parseAssign(self):
        assignnode = node.node()
        targetname = self.token.getText()
        # Symbol table
        varnode = node("VARIABLE")
        varnode.set("ID",targetname)
        assignnode.appendChild(varnode)
        
        if self.token.tokentype == "COLON_EQUALS":
            self.token = self.scanner.gettoken() # consume it
        else:
            self.scanner.mark("Exspected := , not"+self.token.text)
        assignnode.appendChild(self.parseExpression())
        return assignnode
    def parseExpression(self):
        rootnode = self.parseSimpleExpression()
        tokentype = self.token.tokentype
        
        if tokentype in ["EQUALS","NOT_EQUALS","LESS_THAN","LESS_EQUALS","GREATER_THAN","GREATER_EQUALS"]:
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
            opNode.addChild(self.parseSimpleExpresion())
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
            negnode.addChild(rootnode)
            rootnode = negnode
        
    
    
    
test = parser("../examples/STATEMENT1.PAS")
test.parse()