from typing import Any, cast

import libcst as cst
from libcst.metadata import PositionProvider


class LangVisitor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self):
        pass

    def visit_Comment(self, node: cst.Comment):
        print(node)
        print(node.value)
        pos = self.get_metadata(PositionProvider, node)
        line = cast(Any, pos).start.line

        print(line)


with open("./example1.py") as f:
    tree = cst.parse_module(f.read())
    tree = cst.MetadataWrapper(tree)

    # print(tree)

    tree.visit(LangVisitor())
