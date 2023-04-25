import re

from fun_with_ast.exceptions_source_match import BadlySpecifiedTemplateError

from fun_with_ast.source_match import MatchPlaceholder
from fun_with_ast.source_matcher_source_match import SourceMatcher
from fun_with_ast.string_part_placeholder import StringPartPlaceholder
from fun_with_ast.utils_source_match import _GetListDefault
from fun_with_ast.text_placeholder_source_match import TextPlaceholder


class StrSourceMatcher(SourceMatcher):
    """Class to generate the source for an _ast.Str node."""

    def __init__(self, node, starting_parens=None):
        super(StrSourceMatcher, self).__init__(node, starting_parens)
        self.separator_placeholder = TextPlaceholder(r'\s*', '')
        self.quote_parts = []
        self.separators = []
        # If set, will apply to all parts of the string.
        self.quote_type = None
        self.original_quote_type = None
        self.original_s = None

    def _GetMatchedInnerText(self):
        return ''.join(p.inner_text_placeholder.GetSource(self.node)
                       for p in self.quote_parts)

    def Match(self, string):
        remaining_string = self.MatchStartParens(string)
        self._get_original_string()
        part = self._part_place_holder()
        remaining_string = MatchPlaceholder(remaining_string, None, part)
        self.quote_parts.append(part)

        remaining_string = self._handle_multipart(remaining_string)

        self.MatchEndParen(remaining_string)
        if len(self.quote_parts) != 1 :
            raise NotImplementedError('Multi-part strings not yet supported')
        self.original_quote_type = (
            self.quote_parts[0].quote_match_placeholder.matched_text)
        start_paran_text = self.GetStartParenText()
        end_paran_text = self.GetEndParenText()
        start_quote = self.original_quote_type
        end_quote = self.original_quote_type
#        string_body = string[:-len(remaining_string)]
        string_body = self.quote_parts[0].inner_text_placeholder.matched_text
        if string_body != self.original_s:
            raise BadlySpecifiedTemplateError('String body does not match node.s')
        parsed_string = start_paran_text + start_quote + string_body + end_quote + end_paran_text
        return parsed_string

    def _handle_multipart(self, remaining_string):
        while True:
            separator = self.separator_placeholder.Copy()
            trial_string = MatchPlaceholder(remaining_string, None, separator)
            if (not re.match(r'ur"|uR"|Ur"|UR"|u"|U"|r"|R"|"', trial_string) and
                    not re.match(r"ur'|uR'|Ur'|UR'|u'|U'|r'|R'|'", trial_string)):
                break
            remaining_string = trial_string
            self.separators.append(separator)
            part = StringPartPlaceholder()
            remaining_string = MatchPlaceholder(remaining_string, None, part)
            self.quote_parts.append(part)
        return remaining_string

    def GetSource(self):
        # We try to preserve the formatting on a best-effort basis
        if self.original_s is not None and self.original_s != self.node.s:
            self.quote_parts = [self.quote_parts[0]]
            self.quote_parts[0].inner_text_placeholder.matched_text = self.node.s

        if self.original_s is None:
            if not self.quote_type:
                self.quote_type = self.original_quote_type or GetDefaultQuoteType()
            return self.quote_type + self.node.s + self.quote_type

        if self.quote_type:
            for part in self.quote_parts:
                part.quote_match_placeholder.matched_text = self.quote_type

        source_list = [self.GetStartParenText()]
        source_list.append(_GetListDefault(
            self.quote_parts, 0, None).GetSource(None))
        for index in range(len(self.quote_parts[1:])):
            source_list.append(_GetListDefault(
                self.separators, index,
                self.separator_placeholder).GetSource(None))
            source_list.append(_GetListDefault(
                self.quote_parts, index + 1, None).GetSource(None))

        source_list.append(self.GetEndParenText())
        return ''.join(source_list)

    def _get_original_string(self):
        self.original_s = self.node.s

    def _part_place_holder(self):
        return StringPartPlaceholder()