import unittest

import pytest

import create_node
import source_match


class PassMatcherTest(unittest.TestCase):
    def testSimpleReturn(self):
        node = create_node.Return(1)
        string = 'return 1'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matcher_source = matcher.GetSource()
        self.assertEqual(string, matcher_source)

    def testReturnStr(self):
        node = create_node.Return('1')
        string = "return '1'"
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matcher_source = matcher.GetSource()
        self.assertEqual(string, matcher_source)

    def testReturnName(self):
        node = create_node.Return(create_node.Name('a'))
        string = "return a"
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matcher_source = matcher.GetSource()
        self.assertEqual(string, matcher_source)

    def testReturnTuple(self):
        node = create_node.Return(create_node.Tuple(['a', 'b']))
        string = "return (a,b)"
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matcher_source = matcher.GetSource()
        self.assertEqual(string, matcher_source)

    @pytest.mark.xfail(strict=True)
    def testReturnTupleNoParans(self):
        node = create_node.Return(create_node.Tuple(['a', 'b']))
        string = "return a,b"
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matcher_source = matcher.GetSource()
        self.assertEqual(string, matcher_source)
