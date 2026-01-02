class Emitter:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.header = ""
        self.code = ""
        self.tabDepth = 0

    def newline(self):
        self.code += '\n'

    def emit(self, code):
        if len(self.code) > 0 and self.code[-1] == '\n':
            self.code += (self.tabDepth * "   ")
        self.code += code

    def incrementTabDepth(self):
        self.tabDepth += 1

    def decrementTabDepth(self):
        self.tabDepth -= 1
        if self.tabDepth < 0:
            print("TAB DEPTH ERROR")
            exit(1)

    def writeFile(self):
        with open(self.fullPath, 'w') as outputFile:
            outputFile.write(self.header + self.code)