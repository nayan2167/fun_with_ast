import unittest

from manipulate_node import create_node as create_node
from fun_with_ast.dynamic_matcher import GetDynamicMatcher
from manipulate_node.create_node import GetNodeFromInput


class ExprMatcherTest(unittest.TestCase):

    def testBasicMatch(self):
        string2 = 'a.b()\n'
        call_node = GetNodeFromInput(string2)
        matcher2 = GetDynamicMatcher(call_node)
        matcher2.Match(string2)
        source2 = matcher2.GetSource()
        self.assertEqual(source2, string2)