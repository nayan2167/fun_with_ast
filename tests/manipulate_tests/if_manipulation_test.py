import sys
import pytest

from fun_with_ast.common_utils.node_tree_util import IsEmptyModule
from fun_with_ast.get_source import GetSource
from fun_with_ast.source_matchers.matcher_resolver import GetDynamicMatcher
from fun_with_ast.manipulate_node.create_node import GetNodeFromInput
from fun_with_ast.manipulate_node.if_manipulator import ManipulateIfNode, IfManipulatorConfig


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@pytest.fixture(params=[('a.b()\n',0),
                        ('a.c()\n',0),
                        ('a=44',0),
                        ("s='fun_with_ast'",0),
                        ("",0),
                        ('a.b()\n',1),
                        ('a.c()\n',1),
                        ('a=44',1),
                        ("s='fun_with_ast'",1),
                        ("",1),
                        ])
def injected_source(request):
    yield request.param


@pytest.fixture(scope="function", params=[
                        {"body": '   pass\n   z=x\n', "else_body": '   a=1\n', "inject_to": 0, "condition": 'c.d():'},
                        {"body": '   a=1\n', "else_body": '   pass', "inject_to": 0, "condition": 'c.d(): # comment'},
                        {"body": "  if x%2 == 0:\n    print(\"x is a positive even number\")\n  else:\n    print(\"x is a positive odd number\")\n",
                           "else_body": '  a=1', "inject_to": 0, "condition": 'a>2: #comment'},
                        {"body": '#line comment \n   pass #comment 1\n', "else_body": '   a=1 #comment 2',
                        "inject_to": 0, "condition": 'a and not b and not not c:'},
                        {"body":  "  if x%2 == 0:\n    print(\"x is a positive even number\")\n  else:\n    print(\"x is a positive odd number\")\n", "else_body":'  a=1',
                        "inject_to":1, "condition":   '(a and not b) or not (not c):'},
                        {"body": '#line comment \n   pass #comment 1\n', "else_body": '   a=1 #comment 2', "inject_to":1, "condition": 'a+b > c/d+c:'},
                        {"body": '#line comment \n   pass #comment 1\n', "else_body": '   a=1 #comment 2', "inject_to": 0, "condition": 'a+b > c/(d+c):'}

                        ])
def body_and_orelse(request):
    yield request.param

#@pytest.mark.usefixtures(body_and_orelse)
class TestIfManupulation:
    def test_If_Manipulation(self, injected_source, capsys):
        original_if_source = 'if (c.d()):\n   a=1'
        if_node, injected_node = self._create_nodes(capsys, injected_source[0], original_if_source)
        manipulator = ManipulateIfNode(if_node, IfManipulatorConfig(body_index=0, location_in_body_index=injected_source[1]))
        manipulator.add_nodes([injected_node])
        composed_source = self._source_after_composition(if_node, capsys)
        expected_source = self._get_expected_if_source(injected_node, injected_source, original_if_source)
        assert expected_source == composed_source


    def test_If_Else_Manipulation(self, injected_source, capsys):
        original_if_source = 'if ( c.d() ):\n   a=1\nelse:\n   b=2'
        if_node, injected_node = self._create_nodes(capsys, injected_source[0], original_if_source)
        manipulator = ManipulateIfNode(if_node, IfManipulatorConfig(1,1))
        manipulator.add_nodes([injected_node])
        composed_source = self._source_after_composition(if_node, capsys)

        add_new_line = '\n' if not injected_source[0].endswith('\n') else ''
        if not IsEmptyModule(injected_node):
            expected_source = original_if_source.replace('b=2', 'b=2\n   ' + injected_source[0] + add_new_line)
        else:
            expected_source = original_if_source
        assert composed_source == expected_source

    def test_If_elif_AddNode(self, injected_source, capsys):
        original_if_source = 'if ( c.d() ):\n   a=1\nelif e==2:\n   b=2'
        if_node, injected_node = self._create_nodes(capsys, injected_source[0], original_if_source)
        manipulator = ManipulateIfNode(if_node, IfManipulatorConfig(1, 1))
        manipulator.add_nodes([injected_node])
        composed_source = self._source_after_composition(if_node, capsys)
        add_new_line = '\n' if not injected_source[0].endswith('\n') else ''
        if not IsEmptyModule(injected_node):
            expected_source = original_if_source.replace('b=2', 'b=2\n   ' + injected_source[0] + add_new_line)
        else:
            expected_source = original_if_source
        assert composed_source == expected_source

    def test_get_source_body(self, body_and_orelse, capsys):
        body, body_index, orelse, test = self._get_test_pastameters(body_and_orelse)
        original_if_source = 'if ' + test + '\n' + body + 'else:\n' + orelse
        if_node, injected_node = self._create_nodes(capsys, 'pass', original_if_source)
        manipulator = ManipulateIfNode(if_node, IfManipulatorConfig(body_index, 1))
        the_source = manipulator.get_body_orelse_source()
        title = 'Body source:' if body_index == 0 else 'Else source:'
        title = 'test_get_source. ' + title
        self._capture_source(capsys, the_source, title, bcolors.OKGREEN, True)
        if body_index == 0:
            assert the_source == body
        elif body_index == 1:
            assert the_source == orelse
        else:
            raise ValueError("body index can be only 0 or 1")


    def test_switch_body_else(self, body_and_orelse, capsys):
        body, body_index, orelse, test = self._get_test_pastameters(body_and_orelse)
        original_if_source = 'if ' + test + '\n' + body + 'else:\n' + orelse
        if_node,_ = self._create_nodes(capsys, 'pass', original_if_source)
        config = IfManipulatorConfig(0, 1)
        manipulator = ManipulateIfNode(if_node, config)
        body_source = manipulator.get_body_orelse_source()
        self._capture_source(capsys, body_source, 'Original Body source:', bcolors.OKGREEN, True)
        config.body_index = 1
        orig_else_source = manipulator.get_body_orelse_source()
        self._capture_source(capsys, orig_else_source, 'Original Else Source', bcolors.OKGREEN, True)
        assert body_source == body
        assert orig_else_source == orelse
        manipulator.rerplace_body(body_source)
        new_else_source = manipulator.get_body_orelse_source()
        self._capture_source(capsys, new_else_source, 'New Else Source', bcolors.OKCYAN, True)
        assert new_else_source == body_source
        assert new_else_source != orelse
        config.body_index = 0
        manipulator.rerplace_body(orig_else_source)
        new_body_source = manipulator.get_body_orelse_source()
        self._capture_source(capsys, new_body_source, 'New Body Source', bcolors.OKCYAN, True)
        if orig_else_source.endswith('\n'):
            add_new_line_to_new_body = ''
        else:
            add_new_line_to_new_body = '\n'
        assert new_body_source == orig_else_source + add_new_line_to_new_body
        expected_new_if_source = 'if ' + test + '\n' + orelse + add_new_line_to_new_body + 'else:\n' + body
        actual_new_if_source = if_node.matcher.GetSource()
        self._capture_source(capsys, actual_new_if_source, 'New If Source', bcolors.OKCYAN, True)
        assert expected_new_if_source == actual_new_if_source

    def _create_nodes(self, capsys, injected_source, original_if_source):
        self._capture_source(capsys, original_if_source, 'original source:', bcolors.OKBLUE)
        if_node = self._create_if_node(original_if_source)
        injected_node, injected_node_source = self._create_injected_node(injected_source)
        return if_node, injected_node

    def _create_injected_node(self, injected_source):
        injected_node_source = injected_source
        injected_node = GetNodeFromInput(injected_node_source)
        injected_node_matcher = GetDynamicMatcher(injected_node)
        injected_node_matcher.do_match(injected_node_source)
        source_from_matcher = injected_node_matcher.GetSource()
        assert source_from_matcher == injected_node_source
        source_from_get_source = GetSource(injected_node, assume_no_indent=True)
        assert source_from_get_source == injected_node_source
        return injected_node, injected_node_source

    def _create_if_node(self, original_if_source):
        if_node = GetNodeFromInput(original_if_source)
        if_node_matcher = GetDynamicMatcher(if_node)
        if_node_matcher.do_match(original_if_source)
        if_node_source = if_node_matcher.GetSource()
        assert if_node_source == original_if_source
        if_node.matcher = if_node_matcher
        return if_node

    def _capture_source(self, capsys, source, title, color, ignore_ident=False):
        if not ignore_ident:
            compile(source, '<string>', mode='exec')
        print(color + '\n' + title + '\n' + source + bcolors.ENDC)
        out, _ = capsys.readouterr()
        sys.stdout.write(out)

    def _source_after_composition(self, if_node, capsys):
        composed_source = GetSource(if_node, assume_no_indent=True)
        self._capture_source(capsys, composed_source, 'Modified source', bcolors.OKCYAN)
        return composed_source

    def _get_test_pastameters(self, body_and_orelse):
        body = body_and_orelse['body']
        orelse = body_and_orelse['else_body']
        body_index = body_and_orelse['inject_to']
        test = body_and_orelse['condition']
        return body, body_index, orelse, test

    def _get_expected_if_source(self,  injected_node, injected_source, original_if_source):
        add_new_line = '' if injected_source[0].endswith('\n') else '\n'
        if not IsEmptyModule(injected_node):
            if injected_source[1] == 0:
                expected_source = original_if_source.replace('   a=1',
                                                             '   ' + injected_source[0] + add_new_line + '   a=1\n')
            else:
                expected_source = original_if_source.replace('   a=1', '   a=1\n   ' + injected_source[0] + add_new_line)
        else:
            expected_source = original_if_source
        return expected_source
