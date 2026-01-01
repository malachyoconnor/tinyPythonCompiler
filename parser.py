import sys
from lexer import *

# GRAMMAR:
# program ::= {statement}
# statement ::= "PRINT" (expression | string) nl
#     | "IF" comparison "THEN" nl {statement} "ENDIF" nl
#     | "WHILE" comparison "REPEAT" nl {statement} "ENDWHILE" nl
#     | "LABEL" ident nl
#     | "GOTO" ident nl
#     | "LET" ident "=" expression nl
#     | "INPUT" ident nl
# comparison ::= expression (("==" | "!=" | ">" | ">=" | "<" | "<=") expression)+
# expression ::= term {( "-" | "+" ) term}
# term ::= unary {( "/" | "*" ) unary}
# unary ::= ["+" | "-"] primary
# primary ::= number | ident
# nl ::= '\n'+

STATEMENT_KEYWORDS = [TokenType.PRINT, TokenType.IF, TokenType.WHILE, TokenType.LABEL, TokenType.GOTO, TokenType.LET,
                      TokenType.INPUT]


# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()          # Variables declared so far.
        self.labelsDeclared = set()   # Labels declared so far.
        self.labelsGotoed = set()     # Labels goto'ed so far.

        self.curToken = None
        self.peekToken = None
        # Called twice to initialise current and peek.
        self.nextToken()
        self.nextToken()

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.kind

    def checkTokenInList(self, kinds):
        for kind in kinds:
            if self.checkToken(kind):
                return True
        return False

    def consumeOrAbort(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + str(kind) + " token!")
        self.nextToken()

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()

    def abort(self, message):
        sys.exit("Error. " + message)

    def program(self):
        print("PROGRAM")
        while self.checkToken(TokenType.NEWLINE):
            self.nextToken()

        while not self.checkToken(TokenType.EOF):
            self.statement()

        for label in self.labelsGotoed:
            if label not in self.labelsDeclared:
                self.abort("Attempting to GOTO to undeclared label: " + label)

    def statement(self):
        print("STATEMENT-", end='')
        if not self.checkTokenInList(STATEMENT_KEYWORDS):
            self.abort("Expected one of" + " ".join([str(x) for x in STATEMENT_KEYWORDS]) + " token!")

        if self.checkToken(TokenType.PRINT):
            self.printStatement()
        elif self.checkToken(TokenType.IF):
            self.ifStatement()
        elif self.checkToken(TokenType.WHILE):
            self.whileStatement()
        elif self.checkToken(TokenType.LABEL):
            self.labelStatement()
        elif self.checkToken(TokenType.GOTO):
            self.gotoStatement()
        elif self.checkToken(TokenType.LET):
            self.letStatement()
        elif self.checkToken(TokenType.INPUT):
            self.inputStatement()

    def printStatement(self):
        print("PRINT")
        self.consumeOrAbort(TokenType.PRINT)

        if self.checkToken(TokenType.STRING):
            self.nextToken()
        else:
            self.expression()

        self.nl()

    def ifStatement(self):
        print("IF")
        self.consumeOrAbort(TokenType.IF)
        self.comparison()
        self.consumeOrAbort(TokenType.THEN)
        self.nl()
        # Possible statement
        while not self.checkToken(TokenType.ENDIF):
            self.statement()
        self.consumeOrAbort(TokenType.ENDIF)
        self.nl()

    def whileStatement(self):
        print("WHILE")
        self.consumeOrAbort(TokenType.WHILE)
        self.comparison()
        self.consumeOrAbort(TokenType.REPEAT)
        self.nl()
        # Possible statement
        while not self.checkToken(TokenType.ENDWHILE):
            self.statement()

        self.consumeOrAbort(TokenType.ENDWHILE)
        self.nl()

    def labelStatement(self):
        print("LABEL")
        self.consumeOrAbort(TokenType.LABEL)

        self.labelsDeclared.add(self.curToken.text)
        self.consumeOrAbort(TokenType.IDENT)

        self.nl()

    def gotoStatement(self):
        print("GOTO")
        self.consumeOrAbort(TokenType.GOTO)

        self.labelsGotoed.add(self.curToken.text)

        self.consumeOrAbort(TokenType.IDENT)
        self.nl()

    def letStatement(self):
        print("LET")
        self.consumeOrAbort(TokenType.LET)

        self.symbols.add(self.curToken.text)
        self.consumeOrAbort(TokenType.IDENT)

        self.consumeOrAbort(TokenType.EQ)
        self.expression()
        self.nl()

    def inputStatement(self):
        print("INPUT")
        self.consumeOrAbort(TokenType.INPUT)

        self.symbols.add(self.curToken.text)
        self.consumeOrAbort(TokenType.IDENT)

        self.nl()

    def comparison(self):
        print("COMPARISON")
        self.expression()
        # (("==" | "!=" | ">" | ">=" | "<" | "<=") expression) +
        while self.checkTokenInList(
                [TokenType.EQEQ, TokenType.NOTEQ, TokenType.GT, TokenType.GTEQ, TokenType.LT, TokenType.LTEQ]):
            self.nextToken()
            self.expression()

    def expression(self):
        print("EXPRESSION")
        self.term()

        while self.checkToken(TokenType.MINUS) or self.checkToken(TokenType.PLUS):
            self.nextToken()
            self.term()

    def term(self):
        print("TERM")
        self.unary()

        while self.checkToken(TokenType.SLASH) or self.checkToken(TokenType.ASTERISK):
            self.nextToken()
            self.unary()

    def unary(self):
        print("UNARY")
        if self.checkToken(TokenType.PLUS) or self.checkToken(TokenType.MINUS):
            self.nextToken()
        self.primary()

    def primary(self):
        print("PRIMARY")
        if not (self.checkToken(TokenType.NUMBER) or self.checkToken(TokenType.IDENT)):
            self.abort("Expected number or ident token!")

        if self.checkToken(TokenType.IDENT):
            if self.curToken.text not in self.symbols:
                self.abort(f"Referencing variable before assignment: {self.curToken.text}")

        self.nextToken()

    def nl(self):
        print("NEWLINE")
        if not self.checkToken(TokenType.NEWLINE):
            self.abort("Expected newline token!")
        while self.curToken.kind == TokenType.NEWLINE:
            self.nextToken()
