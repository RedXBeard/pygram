# encoding: utf-8

from npyscreen import RoundCheckBox
from npyscreen import Textfield


class CustomRoundCheckBox(RoundCheckBox):
    def whenToggled(self, current_dialog):
        root = self.find_parent_app()
        form = root.getForm('MAIN')
        form.load_history(current_dialog=current_dialog)

    def _create_label_area(self, screen):
        l_a_width = self.width - 3

        if l_a_width < 1:
            raise ValueError("Width of checkbox + label must be at least 6")
        self.label_area = Textfield(screen, rely=self.rely, relx=self.relx + 3,
                                    width=self.width - 3, value=self.name)

    def update(self, clear=True):
        super().update(clear=clear)
        if self.hide: return True
        if self.value:
            cb_display = self.__class__.False_box
        else:
            cb_display = self.__class__.False_box
        if self.do_colors():
            self.parent.curses_pad.addstr(self.rely, self.relx, cb_display,
                                          self.parent.theme_manager.findPair(self, 'CONTROL'))
        else:
            self.parent.curses_pad.addstr(self.rely, self.relx, cb_display)

        self._update_label_area()

    def calculate_area_needed(self):
        return 0, 0
