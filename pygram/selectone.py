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

    def display_value(self, vl):
        try:
            if isinstance(vl, DictObject):
                return self.safe_string(vl.printed)
            return self.safe_string(str(vl))
        except ReferenceError:
            return "**REFERENCE ERROR**"
