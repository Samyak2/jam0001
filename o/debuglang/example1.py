from parser import parser

program1 = """(+ 1 2)"""

ast = parser.parse(program1)

print(ast.pretty())
