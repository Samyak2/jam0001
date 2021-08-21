from lark import Lark

with open("grammar.lark", "r") as f:
    parser = Lark(f.read(), start="start", parser='lalr')
