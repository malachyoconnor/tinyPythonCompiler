from lexer import *
from emitter import *
from parser import *

def main():
    # f = open('fib_program.txt', 'r')
    # scriptText = f.read()
    scriptText = open('test_expressionSimple.txt', 'r').read()

    lexer = Lexer(scriptText)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()
    emitter.writeFile()
    print("Parsing completed!")


main()