import _ast

from fun_with_ast.exceptions_source_match import BadlySpecifiedTemplateError

from fun_with_ast.create_node import SyntaxFreeLine

from fun_with_ast.placeholder_source_match import Placeholder
from fun_with_ast.string_parser import StringParser
from fun_with_ast.node_placeholder_source_match import NodePlaceholder


class CompositePlaceholder(Placeholder):
    """Node which wraps one or more other nodes."""

    def Match(self, node, string):
        """Makes sure node.(self.field_name) is in string."""
        self.Validate(node)
        elements = self.GetElements(node)
        parser = StringParser(
            string, elements, starting_parens=self.starting_parens)
        return parser.GetMatchedText()

    def GetSource(self, node):
        return ''.join(
            element.GetSource(node) for element in self.GetElements(node))

    def Validate(self, unused_node):
        return True

class ListFieldPlaceholder(CompositePlaceholder):
    """Placeholder for a field which is a list of child nodes."""

    def __init__(self, field_name,
                 before_placeholder=None, after_placeholder=None,
                 prefix_placeholder=None,
                 exclude_first_before=False):
        """Initializes a field which is a list of child nodes.

        Args:
          field_name: {str} The name of the field
          before_placeholder: {TextPlaceholder} Text to expect to come before the
            child element.
          after_placeholder: {TextPlaceholder} Text to expect to come after the
            child element.
          prefix_placeholder: {TextPlaceholder} Text to expect to come before
            the list.
          exclude_first_before: {bool} Whether to exclude the last
            before_placholder, used for SeparatorListFieldPlaceholder.
        """
        super(ListFieldPlaceholder, self).__init__()
        self.field_name = field_name
        self.prefix_placeholder = prefix_placeholder
        self.before_placeholder = before_placeholder
        self.after_placeholder = after_placeholder
        self.exclude_first_before = exclude_first_before
        self.matched_before = []
        self.matched_after = []

    def _GetBeforePlaceholder(self, index):
        if index < len(self.matched_before):
            return self.matched_before[index]
        new_placeholder = self.before_placeholder.Copy()
        self.matched_before.append(new_placeholder)
        return new_placeholder

    def _GetAfterPlaceholder(self, index):
        if index < len(self.matched_after):
            return self.matched_after[index]
        new_placeholder = self.after_placeholder.Copy()
        self.matched_after.append(new_placeholder)
        return new_placeholder

    def GetValueAtIndex(self, values, index):
        """Gets the set of node in values at index, including before and after."""
        elements = []
        child_value = values[index]
        if isinstance(child_value, SyntaxFreeLine):
            return [NodePlaceholder(child_value)]
        if (self.before_placeholder and
                not (self.exclude_first_before and index == 0)):
            before_index = index - 1 if self.exclude_first_before else index
            elements.append(self._GetBeforePlaceholder(before_index))
        elements.append(NodePlaceholder(child_value))
        if self.after_placeholder:
            elements.append(self._GetAfterPlaceholder(index))
        return elements

    def GetElements(self, node):
        field_value = getattr(node, self.field_name) or []
        elements = []
        if self.prefix_placeholder and field_value:
            elements.append(self.prefix_placeholder)
        for i in range(len(field_value)):
            elements.extend(self.GetValueAtIndex(field_value, i))
        return elements

    def Validate(self, node):
        field_value = getattr(node, self.field_name)
        if field_value and not isinstance(field_value, (list, tuple)):
            raise BadlySpecifiedTemplateError(
                'Field {} of node {} is a not list, so please use a FieldPlaceholder'
                'instead of a ListFieldPlaceholder'.format(self.field_name, node))

    def __repr__(self):
        return ('ListFieldPlaceholder for field "{}" with before placeholder "{}"'
                'and after placeholder "{}"'.format(
            self.field_name, self.before_placeholder,
            self.after_placeholder))

class FieldPlaceholder(CompositePlaceholder):
    """Placeholder for a field."""

    def __init__(
            self, field_name, before_placeholder=None):
        super(FieldPlaceholder, self).__init__()
        self.field_name = field_name
        self.before_placeholder = before_placeholder

    def GetElements(self, node):
        if isinstance(node, _ast.Call) and self.field_name == 'kwargs':
            field_value = getattr(node, self.field_name, None)
        else:
            field_value = getattr(node, self.field_name)

        if not field_value:
            return []

        elements = []
        if self.before_placeholder:
            elements.append(self.before_placeholder)
        elements.append(NodePlaceholder(field_value))
        return elements

    def Match(self, node, string):
        return super(FieldPlaceholder, self).Match(node, string)

    def Validate(self, node):
        if isinstance(node, _ast.Call) and self.field_name == 'kwargs':
            field_value = getattr(node, self.field_name, None)
        else:
            field_value = getattr(node, self.field_name)
        if isinstance(field_value, (list, tuple)):
            raise BadlySpecifiedTemplateError(
                'Field {} of node {} is a list. please use a ListFieldPlaceholder'
                'instead of a FieldPlaceholder'.format(self.field_name, node))

    def __repr__(self):
        return 'FieldPlaceholder for field "{}"'.format(
            self.field_name)
