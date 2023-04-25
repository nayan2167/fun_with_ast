from fun_with_ast.exceptions_source_match import BadlySpecifiedTemplateError

from fun_with_ast.get_source import GetSource
from fun_with_ast.placeholder_source_match import Placeholder
#from source_match import ValidateStart
from fun_with_ast.string_parser import StripStartParens


def ValidateStart(full_string, starting_string):
    stripped_full = StripStartParens(full_string)
    stripped_start = StripStartParens(starting_string)
    if not stripped_full.startswith(stripped_start):
        raise BadlySpecifiedTemplateError(
            'String "{}" should have started with string "{}"'
                .format(stripped_full, stripped_start))
    return True

class NodePlaceholder(Placeholder):
    """Placeholder to wrap an AST node."""

    def __init__(self, node):
        super(NodePlaceholder, self).__init__()
        self.node = node

    def Match(self, unused_node, string):
        node_src = GetSource(self.node, string, self.starting_parens)
        ValidateStart(string, node_src)
        return node_src

    def GetSource(self, unused_node):
        return GetSource(self.node)