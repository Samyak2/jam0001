from typing import Any, List, cast, Tuple

import libcst as cst
from libcst.metadata import PositionProvider


class CommentExtractor(cst.CSTVisitor):
    METADATA_DEPENDENCIES = (PositionProvider,)

    def __init__(self):
        self.comments: List[Tuple[str, int]] = []

    def visit_Comment(self, node: cst.Comment):
        pos = self.get_metadata(PositionProvider, node)
        line = cast(Any, pos).start.line

        self.comments.append((node.value, line))


def extract_comments(filename):
    with open(filename) as f:
        tree = cst.parse_module(f.read())

    tree = cst.MetadataWrapper(tree)

    # print(tree)
    commentExtractor = CommentExtractor()

    tree.visit(commentExtractor)

    return commentExtractor.comments


if __name__ == "__main__":

    print(extract_comments("example2.py"))
