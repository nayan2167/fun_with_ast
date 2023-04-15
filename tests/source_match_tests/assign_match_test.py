import unittest

import pytest

import create_node
import source_match


class AssignMatcherTest(unittest.TestCase):

    def testBasicMatchAssignHex(self):
        node = create_node.Assign('a', create_node.Num(0x1F))
        string = 'a=0x1F'
        matcher = source_match.GetMatcher(node)
        with pytest.raises(NotImplementedError):
            matcher.Match(string)

    def testBasicNotMatchAssignTrailingWS(self):
        node = create_node.Assign('a', create_node.Num(1))
        string = 'a=1 '
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testBasicMatchAssignWithWSAndTab(self):
        node = create_node.Assign('a', create_node.Num(1))
        string = ' a  =  1  \t'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    #@pytest.mark.xfail(strict=True)
    def testMatchMultiAssign(self):
        node = create_node.Assign(['a', 'b'], create_node.Num(2))
        string = 'a=b=1'
        matcher = source_match.GetMatcher(node)
        matched_string = matcher.GetSource()
        self.assertNotEqual(string, matched_string)

    def testNotMatchMultiAssign(self):
        node = create_node.Assign(['a', 'b'], create_node.Num(1))
        string = 'a=c=1'
        matcher = source_match.GetMatcher(node)
        matched_string = matcher.GetSource()
        self.assertNotEqual(string, matched_string)


    def testMatchMultiAssignWithWS(self):
        node = create_node.Assign(['a', 'b'], create_node.Num(1))
        string = 'a\t=\t     b \t  =1 \t'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testMatchMultiAssignWithWSAndComment(self):
        node = create_node.Assign(['a', 'b'], create_node.Num(1))
        string = 'a\t=\t     b \t  =1 \t #comment'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    @pytest.mark.xfail(strict=True)
    def testMatchMultiAssignNameWithWSAndComment(self):
        node = create_node.Assign(['a', 'b'], create_node.Name('c'))
        string = 'a\t=\t     b \t  =c \t #comment'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testNotMatchMultiAssignWithWS(self):
        node = create_node.Assign(['a', 'b'], create_node.Num(1))
        string = 'a\t=\t     bb \t  =1 \t'
        matcher = source_match.GetMatcher(node)
        with pytest.raises(source_match.BadlySpecifiedTemplateError):
            matcher.Match(string)

