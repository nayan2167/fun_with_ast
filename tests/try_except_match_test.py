import unittest

import create_node
import source_match


class TryExceptMatcherTest(unittest.TestCase):

    def testBasicMatch(self):
        node = create_node.Try(
            [create_node.Pass()],
            [create_node.ExceptHandler(None, None, [create_node.Pass()])])

        string = """try:\n\tpass\nexcept:\n\tpass\n"""
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())


    def testMatchMultipleExceptHandlers(self):
        node = create_node.Try(
            [create_node.Expr(create_node.Name('a'))],
            [create_node.ExceptHandler('TestA'),
             create_node.ExceptHandler('TestB')])
        string = """try:
  a 
except TestA:
  pass
except TestB:
  pass
"""
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testMatchExceptAndOrElse(self):
        node = create_node.Try(
            [create_node.Expr(create_node.Name('a'))],
            [create_node.ExceptHandler()],
            orelse=[create_node.Pass()])
        string = """try:
  a
except:
  pass
else:
  pass
"""
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())

    def testMatchWithEmptyLine(self):
        node = create_node.Try(
            [create_node.Expr(create_node.Name('a'))],
            [create_node.ExceptHandler('Exception1', 'e')])
        string = """try:
  a

except Exception1 as e:

  pass
"""
        matcher = source_match.GetMatcher(node)
        matcher.Match(string)
        self.assertEqual(string, matcher.GetSource())
