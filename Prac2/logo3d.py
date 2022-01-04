import sys
from subprocess import call
from antlr4 import *
from logo3dLexer import logo3dLexer
from logo3dParser import logo3dParser
from visitor import visitor


def main(argv):
    input_stream = FileStream(argv[1])
    lexer = logo3dLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = logo3dParser(token_stream)
    tree = parser.root()
    # Si no se especifica la función por la que empezar, por defecto se empieza por la función main
    if len(argv) < 3:
        vis = visitor(tree, ['main'])
    else:
        vis = visitor(tree, argv[2:])
    res = vis.visit(tree)


if __name__ == '__main__':
    main(sys.argv)
