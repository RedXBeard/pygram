# encoding: utf-8

from npyscreen import RoundCheckBox
from npyscreen import Textfield


class CustomRoundCheckBox(RoundCheckBox):
    def __init__(self, screen, value=False, **keywords):
        super().__init__(screen, value=value, **keywords)
        self.unread = None

    def when_toggle(self, current_dialog):
        root = self.find_parent_app()
        form = root.getForm('MAIN')
        form.load_history(current_dialog=current_dialog)

    def _create_label_area(self, screen):
        l_a_width = self.width - 5

        if l_a_width < 1:
            raise ValueError("Width of checkbox + label must be at least 6")
        self.label_area = Textfield(screen, rely=self.rely, relx=self.relx + 5,
                                    width=self.width - 5, value=self.name)

    def update(self, clear=True):
        super().update(clear=clear)
        if self.hide:
            return True
        cb_display = "({})".format(str(self.unread).zfill(2))
        if self.do_colors():
            self.parent.curses_pad.addstr(self.rely, self.relx, cb_display,
                                          self.parent.theme_manager.findPair(
                                              self, 'DANGER' if self.unread else 'CONTROL'))
        else:
            self.parent.curses_pad.addstr(self.rely, self.relx, cb_display)

        self._update_label_area()

    def _update_label_row_attributes(self, row, clear=True):
        super()._update_label_row_attributes(row, clear=clear)
        if self.unread:
            row.color = 'DANGER'
        else:
            row.color = 'DEFAULT'

        row.update(clear=clear)

    def calculate_area_needed(self):
        return 0, 0
