import sys
from antlr4 import *
from teamplusplusLexer import teamplusplusLexer
from teamplusplusParser import teamplusplusParser
 
class MyGrammarListener(ParseTreeListener):
    def enterKey(self, ctx):
        pass
    def exitKey(self, ctx):
        pass
    def enterValue(self, ctx):
        pass
    def exitValue(self, ctx):
        pass
    
class KeyPrinter(MyGrammarListener):     
    def exitKey(self, ctx):         
        print("Oh, a key!") 

def main(argv):
    fileName = "test.txt"

    input_stream = FileStream(fileName)
    lexer = teamplusplusLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = teamplusplusParser(stream)
    tree = parser.programa()
    printer = KeyPrinter()
    walker = ParseTreeWalker()
    walker.walk(printer, tree)
 
if __name__ == '__main__':
    main(sys.argv)