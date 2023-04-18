# A mapping of node_type: expected_parts
import _ast
import sys

from fun_with_ast.source_match import DefaultSourceMatcher

import fun_with_ast.create_node
def GetDynamicMatcher(node, starting_parens=None):
    """Gets an initialized matcher for the given node (doesnt call .Match).

    If there is no corresponding matcher in _matchers, this will return a
    default matcher, which starts with a placeholder for the first field, ends
    with a placeholder for the last field, and includes TextPlaceholders
    with '.*' regexes between.

    Args:
      node: The node to get a matcher for.
      starting_parens: The parens the matcher may start with.

    Returns:
      A matcher corresponding to that node, or the default matcher (see above).
    """
    if starting_parens is None:
        starting_parens = []
#    parts_or_matcher = _matchers[node.__class__]
    parts_or_matcher_string = _dynamic_matchers[node.__class__]
#    current_module = sys.modules[__name__]
    current_module = sys.modules['fun_with_ast.source_match']
    parts_or_matcher = getattr(current_module, parts_or_matcher_string)
    try:
        parts = parts_or_matcher()
        return DefaultSourceMatcher(node, parts, starting_parens)
    except TypeError:
        matcher = parts_or_matcher(node, starting_parens)
        return matcher

_dynamic_matchers = {
    _ast.Add: 'get_Add_expected_parts',
    _ast.alias: 'get_alias_expected_parts',
    _ast.And: 'get_And_expected_parts',
    _ast.Assert: 'get_Assert_expected_parts',
    _ast.Assign: 'get_Assign_expected_parts',
    _ast.Attribute: 'get_Attribute_expected_parts',
    _ast.AugAssign: 'get_AugAssign_expected_parts',
    _ast.arguments: 'get_arguments_expected_parts',
    _ast.arg: 'get_arg_expected_parts',
    _ast.BinOp: 'get_BinOp_expected_parts',
    _ast.BitAnd: 'get_BitAnd_expected_parts',
    _ast.BitOr: 'get_BitOr_expected_parts',
    _ast.BitXor: 'get_BitXor_expected_parts',
    _ast.BoolOp: 'BoolOpSourceMatcher',
    _ast.Break: 'get_Break_expected_parts',
    _ast.Call: 'get_Call_expected_parts',
    _ast.ClassDef: 'get_ClassDef_expected_parts',
    _ast.Compare: 'get_Compare_expected_parts',
    _ast.comprehension: 'get_comprehension_expected_parts',
    _ast.Continue: 'get_Continue_expected_parts',
    _ast.Delete: 'get_Delete_expected_parts',
    _ast.Dict: 'get_Dict_expected_parts',
    _ast.DictComp: 'get_DictComp_expected_parts',
    _ast.Div: 'get_Div_expected_parts',
    _ast.Eq: 'get_Eq_expected_parts',
    _ast.Expr: 'get_Expr_expected_parts',
    _ast.ExceptHandler: 'get_ExceptHandler_expected_parts',
    _ast.FloorDiv: 'get_FloorDiv_expected_parts',
    _ast.For: 'get_For_expected_parts',
    _ast.FunctionDef: 'get_FunctionDef_expected_parts',
    _ast.GeneratorExp: 'get_GeneratorExp_expected_parts',
    _ast.Global: 'get_Global_expected_parts',
    _ast.Gt: 'get_Gt_expected_parts',
    _ast.GtE: 'get_GtE_expected_parts',
    _ast.If: 'IfSourceMatcher',
    _ast.IfExp: 'get_IfExp_expected_parts',
    _ast.Import: 'get_Import_expected_parts',
    _ast.ImportFrom: 'get_ImportFrom_expected_parts',
    _ast.In: 'get_In_expected_parts',
    #    _ast.Index: get_Index_expected_parts',
    _ast.Invert: 'get_Invert_expected_parts',
    _ast.Is: 'get_Is_expected_parts',
    _ast.IsNot: 'get_IsNot_expected_parts',
    _ast.keyword: 'get_keyword_expected_parts',
    _ast.Lambda: 'get_Lambda_expected_parts',
    _ast.List: 'get_List_expected_parts',
    _ast.ListComp: 'get_ListComp_expected_parts',
    _ast.LShift: 'get_LShift_expected_parts',
    _ast.Lt: 'get_Lt_expected_parts',
    _ast.LtE: 'get_LtE_expected_parts',
    _ast.Mod: 'get_Mod_expected_parts',
    _ast.Module: 'get_Module_expected_parts',
    _ast.Mult: 'get_Mult_expected_parts',
    _ast.Name: 'get_Name_expected_parts',
    _ast.Not: 'get_Not_expected_parts',
    _ast.NotIn: 'get_NotIn_expected_parts',
    _ast.NotEq: 'get_NotEq_expected_parts',
    #    _ast.Num: NumSourceMatcher',
    _ast.Or: 'get_Or_expected_parts',
    _ast.Pass: 'get_Pass_expected_parts',
    _ast.Pow: 'get_Pow_expected_parts',
    #    _ast.Print: get_Print_expected_parts',
    _ast.Raise: 'get_Raise_expected_parts',
    _ast.Return: 'get_Return_expected_parts',
    _ast.RShift: 'get_RShift_expected_parts',
    _ast.Slice: 'get_Slice_expected_parts',
    _ast.Sub: 'get_Sub_expected_parts',
    _ast.Set: 'get_Set_expected_parts',
    _ast.SetComp: 'get_SetComp_expected_parts',
    _ast.Subscript: 'get_Subscript_expected_parts',
    #    _ast.Str: 'StrSourceMatcher',
    _ast.Constant: 'ConstantSourceMatcher',
    fun_with_ast.create_node.SyntaxFreeLine: 'get_SyntaxFreeLine_expected_parts',
    fun_with_ast.create_node.Comment: 'get_Comment_expected_parts',
    _ast.Tuple: 'TupleSourceMatcher',
    #    _ast.TryExcept: get_TryExcept_expected_parts',
    #    _ast.Try: TryFinallySourceMatcher',
    _ast.JoinedStr: 'get_JoinedStr_expected_parts',
    _ast.Try: 'get_TryExcept_expected_parts',
    _ast.UAdd: 'get_UAdd_expected_parts',
    _ast.UnaryOp: 'get_UnaryOp_expected_parts',
    _ast.USub: 'get_USub_expected_parts',
    _ast.While: 'get_While_expected_parts',
    _ast.With: 'WithSourceMatcher',
    _ast.withitem: 'WithItemSourceMatcher',
    _ast.Yield: 'get_Yield_expected_parts'
}
