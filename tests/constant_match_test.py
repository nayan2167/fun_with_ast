import unittest

import pytest
from fun_with_ast.source_match import BadlySpecifiedTemplateError

import create_node
import source_match


class ConstantMatcherTest(unittest.TestCase):

    def testBasicMatchNum(self):
        node = create_node.Num('1')
        string = '1'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)


    def testBasicMatchStr(self):
        node = create_node.Str('1')
        string = "'1'"
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testBasicMatchStrWithWS(self):
        node = create_node.Str('  1  ')
        string = "'  1  '"
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testBasicNoMatchStr(self):
        node = create_node.Str('1')
        string = "'2'"
        matcher = source_match.GetMatcher(node)
        with pytest.raises(BadlySpecifiedTemplateError):
            matcher.Match(string)

    def testBasicMatchWithPlusSign(self):
        node = create_node.Num('1')
        string = '+1'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testBasicMatchWithMinusSign(self):
        node = create_node.Num('-1')
        string = '  -1   \t'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testBasicMatchWithdWS(self):
        node = create_node.Num('1')
        string = '   1   '
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testMatchWSWithComment(self):
        node = create_node.Num('1')
        string = '   1   #comment'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testWithParans(self):
        node = create_node.Num('1')
        string = '(1)'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testWithParansAndWS(self):
        node = create_node.Num('1')
        string = '(   1   )     '
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testWithMultiParansAndWS(self):
        node = create_node.Num('1')
        string = '((   1   )    ) '
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testNoMatchMultiParansAndWS(self):
        node = create_node.Num('1')
        string = '((   1   )     '
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertNotEqual(string, matcher.GetSource())

    def testLargeNumberMatch(self):
        node = create_node.Num('1234567890987654321')
        string = '1234567890987654321'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testBasicNoMatchNum(self):
        node = create_node.Num('2')
        string = '1'
        matcher = source_match.GetMatcher(node)
        with pytest.raises(source_match.BadlySpecifiedTemplateError):
            matcher.Match(string)
        string = '2'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())


    def testMatchBool(self):
        node = create_node.Bool(False)
        string = 'False'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testMatchBoolParans(self):
        node = create_node.Bool(False)
        string = '(False)'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())
