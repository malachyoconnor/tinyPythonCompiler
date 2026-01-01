from lexer import *
from emitter import *
from parser import *
import subprocess

def main():
    scriptName = input("Please enter the name of the script (without .txt): ")
    scriptText = open(f"{scriptName}.txt", 'r').read()

    lexer = Lexer(scriptText)
    emitter = Emitter("out.c")
    parser = Parser(lexer, emitter)

    parser.program()
    emitter.writeFile()
    print("Parsing completed!")

    subprocess.call(['bat', '-s', '--paging=never', './out.c'])


main()
