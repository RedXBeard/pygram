# encoding: utf-8

from DictObject import DictObject
from npyscreen import SelectOne

from pygram.checkbox import CustomRoundCheckBox


class CustomSelectOne(SelectOne):
    _contained_widgets = CustomRoundCheckBox

    def h_select(self, ch):
        self.value = [self.cursor_line, ]
        line = self._my_widgets[self.value[0]]
        line.whenToggled(self.values[self.value[0]])

    def _print_line(self, line, value_indexer):
        try:
            unread, display_this = self.display_value(self.values[value_indexer])
            if unread > 1:
                unread = '1+'
            line.value = display_this
            line.hide = False
            if hasattr(line, 'selected'):
                line.selected = bool(value_indexer in self.value and (self.value is not None))
            # Most classes in the standard library use this
            else:
                line.show_bold = False
                line.value = False
                if value_indexer in self.value and (self.value is not None):
                    line.show_bold = True
                    line.value = True
                line.name = display_this
            line.unread = unread
            line.important = bool(value_indexer in self._filtered_values_cache)
        except IndexError:
            line.name = None
            line.hide = True

        line.highlight = False

    def display_value(self, vl):
        try:
            if isinstance(vl, DictObject):
                return vl.unread, self.safe_string(vl.printed)
            return self.safe_string(str(vl))
        except ReferenceError:
            return "**REFERENCE ERROR**"

    def update(self, clear=True):
        super().update(clear=clear)
        for widget in self._my_widgets:
            widget.update()
