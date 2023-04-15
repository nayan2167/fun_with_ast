import unittest

import pytest

import create_node
import source_match


class NameMatcherTest(unittest.TestCase):

    def testBasicMatch(self):
        node = create_node.Name('foobar')
        string = 'foobar'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testBasicMatchWithWS(self):
        node = create_node.Name('foobar')
        string = ' \t  foobar \t'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    @pytest.mark.xfail(strict=True)
    def testBasicMatchWithWSAndComment(self):
        node = create_node.Name('foobar')
        string = ' \t  foobar \t #comment'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testBasicMatchOnlyComment(self):
        node = create_node.Name('foobar')
        string = ' \t  foobar#comment'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testBasicMatchOnlyComment(self):
        node = create_node.Name('foobar')
        string = ' \t #comment  foobar'
        matcher = source_match.GetMatcher(node)
        with pytest.raises(source_match.BadlySpecifiedTemplateError):
            matcher.Match(string)

    def testIdChange(self):
        node = create_node.Name('foobar')
        string = 'foobar'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        node.id = 'hello'
        self.assertEqual('hello', matcher.GetSource())


    def testBasicMatch2(self):
        node = create_node.Name('a')
        string = 'a'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testMatchWithWS(self):
        node = create_node.Name('a')
        string = 'a '
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    @pytest.mark.xfail(strict=True)
    def testMatchWithComment(self):
        node = create_node.Name('a')
        string = 'a # comment'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_string = matcher.GetSource()
        self.assertEqual(string, matched_string)

    def testLeadingSpaces(self):
        node = create_node.Name('a')
        string = '  a'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_text = matcher.GetSource()
        self.assertEqual(string, matched_text)
        string = ' \t  a'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        matched_text = matcher.GetSource()
        self.assertEqual(string, matched_text)
        string = ' \t\n  a'
        matcher = source_match.GetMatcher(node)
        with self.assertRaises(source_match.BadlySpecifiedTemplateError):
            matcher.Match(string)

