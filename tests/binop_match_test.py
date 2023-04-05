import unittest

import pytest

import create_node
import source_match


class BinOpMatcherTest(unittest.TestCase):

    def testAddBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.Add(),
            create_node.Name('b'))
        string = 'a + b'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testAddBinOpNegativeTest(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.Add(),
            create_node.Name('b'))
        string = 'b + a'
        matcher = source_match.GetMatcher(node)
        with pytest.raises(source_match.BadlySpecifiedTemplateError):
            matcher.Match(string)

    def testSubBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.Sub(),
            create_node.Num('1'))
        string = '\ta - 1  \t'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testSubBinOpNegativeTest(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.Sub(),
            create_node.Num('2'))
        string = '\t  a - 1'
        matcher = source_match.GetMatcher(node)
        with pytest.raises(source_match.BadlySpecifiedTemplateError):
            matcher.Match(string)

    def testMultBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.Mult(),
            create_node.Name('b'))
        string = 'a * b'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testDivBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.Div(),
            create_node.Name('b'))
        string = ' a    /        b '
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testFloorDivBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.FloorDiv(),
            create_node.Name('b'))
        string = '  \t a // \t b  \t'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testFloorDivBinOpWithComment(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.FloorDiv(),
            create_node.Num('1'))
        string = '  \t a // \t 1  \t #comment'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testModBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.Mod(),
            create_node.Name('b'))
        string = 'a % b    '
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testPowBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.Pow(),
            create_node.Name('b'))
        string = 'a ** b'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testLShiftBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.LShift(),
            create_node.Name('b'))
        string = 'a << b'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testRShiftBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.RShift(),
            create_node.Name('b'))
        string = 'a >> b'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testBitOrBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.BitOr(),
            create_node.Name('b'))
        string = 'a | b'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testBitXorBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.BitXor(),
            create_node.Name('b'))
        string = 'a ^ b'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testBitAndBinOp(self):
        node = create_node.BinOp(
            create_node.Name('a'),
            create_node.BitAnd(),
            create_node.Name('b'))
        string = 'a & b'
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())
