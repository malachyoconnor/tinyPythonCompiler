import enum

class Trie:
    def __init__(self):
        self.root = {}
        self.endOfWord = "\\"

    def insert(self, word):
        node = self.root
        for char in word:
            node = node.setdefault(char, {})
        node[self.endOfWord] = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node:
                return False
            node = node[char]
        return self.endOfWord in node

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node:
                return False
            node = node[char]
        return True

class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText  # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind  # The TokenType that this token is classified as.

# TokenType is our enum for all the types of tokens.
class TokenType(enum.Enum):
    EOF = -1                       # DONE
    NEWLINE = 0                    # DONE
    NUMBER = 1                     # DONE
    IDENT = 2                      # DONE
    STRING = 3                     # DONE
    # Keywords.                    #
    LABEL = 101                    # DONE
    GOTO = 102                     # DONE
    PRINT = 103                    # DONE
    INPUT = 104                    # DONE
    LET = 105                      # DONE
    IF = 106                       # DONE
    THEN = 107                     # DONE
    ENDIF = 108                    # DONE
    WHILE = 109                    # DONE
    REPEAT = 110                   # DONE
    ENDWHILE = 111                 # DONE
    # Operators.
    EQ = 201                       # DONE
    PLUS = 202                     # DONE
    MINUS = 203                    # DONE
    ASTERISK = 204                 # DONE
    SLASH = 205                    # DONE
    EQEQ = 206                     # DONE
    NOTEQ = 207                    # DONE
    LT = 208                       # DONE
    LTEQ = 209                     # DONE
    GT = 210                       # DONE
    GTEQ = 211                     # DONE


class Lexer:
    def __init__(self, source):
        self.currentPos = -1
        self.currentChar = ''
        self.source = source + '\n'
        self.keyWordTrie = Trie()
        for keyword in ["LABEL", "GOTO", "PRINT", "INPUT", "LET", "IF", "THEN", "ENDIF", "WHILE", "REPEAT", "ENDWHILE"]:
            self.keyWordTrie.insert(keyword)
        self.nextChar()

    # Process the next character.
    def nextChar(self):
        self.currentPos += 1
        if self.currentPos < len(self.source):
            self.currentChar = self.source[self.currentPos]
        else:
            self.currentChar = '\0'

    # Return the lookahead character.
    def peek(self):
        if self.currentPos + 1 < len(self.source):
            return self.source[self.currentPos + 1]
        return '\0'

    # Invalid token found, print error message and exit.
    def abort(self, message):
        print("ERROR: " + message)
        exit(1)

    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.currentPos < len(self.source) and self.source[self.currentPos].isspace():
            self.nextChar()

    # Skip comments in the code.
    def skipComment(self):
        while self.currentPos < len(self.source) and self.source[self.currentPos] != '\n':
            self.nextChar()

    # Return the next token.
    def getToken(self) -> Token:
        result = None
        if self.currentChar == '\0':
            result = Token('\0', TokenType.EOF)
        # Note: This check MUST occur before the whitespace check
        elif self.currentChar == '\n':
            result = Token('\\n', TokenType.NEWLINE)
        elif self.currentChar.isspace():
            self.skipWhitespace()
            return self.getToken()
        elif self.currentChar == '#':
            self.skipComment()
            return self.getToken()
        elif self.currentChar == '=' and self.peek() == '=':
            result = Token('==', TokenType.EQEQ)
        elif self.currentChar == '!' and self.peek() == '=':
            result = Token('!=', TokenType.NOTEQ)
        elif self.currentChar == '>' and self.peek() == '=':
            result = Token('>=', TokenType.GTEQ)
        elif self.currentChar == '<' and self.peek() == '=':
            result = Token('<=', TokenType.LTEQ)
        elif self.currentChar == '+':
            result = Token('+', TokenType.PLUS)
        elif self.currentChar == '-':
            result = Token('-', TokenType.MINUS)
        elif self.currentChar == '*':
            result = Token('*', TokenType.ASTERISK)
        elif self.currentChar == '/':
            result = Token('/', TokenType.SLASH)
        elif self.currentChar == '=':
            result = Token('=', TokenType.EQ)
        elif self.currentChar == '>':
            result = Token('>', TokenType.GT)
        elif self.currentChar == '<':
            result = Token('<', TokenType.LT)
        elif self.currentChar.isdigit():
            fullNumber = ""
            decimalUsed = False
            while self.currentChar.isdigit() or self.currentChar == '.':
                if self.currentChar == '.':
                    if decimalUsed:
                        self.abort(f"Two decimal places observed in number: '{fullNumber}.'")
                    decimalUsed = True
                fullNumber += self.currentChar
                self.nextChar()
            return Token(fullNumber, TokenType.NUMBER)
        elif self.currentChar == '\"':
            fullString = ""
            self.nextChar()
            while self.currentChar != '\"':
                if self.currentChar == '\r' or self.currentChar == '\n' or self.currentChar == '\t' or self.currentChar == '\\' or self.currentChar == '%':
                    self.abort(f"Illegal character in string: '{self.currentChar}'")
                fullString += self.currentChar
                self.nextChar()
            self.nextChar()
            return Token(fullString, TokenType.STRING)
        elif self.currentChar.isalpha():
            fullKeyword = self.currentChar
            self.nextChar()
            while self.currentChar.isalpha() and self.keyWordTrie.starts_with(fullKeyword):
                fullKeyword += self.currentChar
                self.nextChar()

            if self.keyWordTrie.search(fullKeyword):
                if fullKeyword == "LABEL":
                    return Token("LABEL", TokenType.LABEL)
                if fullKeyword == "GOTO":
                    return Token("GOTO", TokenType.GOTO)
                if fullKeyword == "PRINT":
                    return Token("PRINT", TokenType.PRINT)
                if fullKeyword == "INPUT":
                    return Token("INPUT", TokenType.INPUT)
                if fullKeyword == "LET":
                    return Token("LET", TokenType.LET)
                if fullKeyword == "IF":
                    return Token("IF", TokenType.IF)
                if fullKeyword == "THEN":
                    return Token("THEN", TokenType.THEN)
                if fullKeyword == "ENDIF":
                    return Token("ENDIF", TokenType.ENDIF)
                if fullKeyword == "WHILE":
                    return Token("WHILE", TokenType.WHILE)
                if fullKeyword == "REPEAT":
                    return Token("REPEAT", TokenType.REPEAT)
                if fullKeyword == "ENDWHILE":
                    return Token("ENDWHILE", TokenType.ENDWHILE)

            while self.currentChar.isalpha():
                fullKeyword += self.currentChar
                self.nextChar()

            return Token(fullKeyword, TokenType.IDENT)

        self.nextChar()
        return result