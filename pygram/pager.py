# encoding: utf-8

import textwrap

from npyscreen import Pager
from npyscreen import wgwidget


class CustomPager(Pager):
    def __init__(self, screen, autowrap=True, center=False, **keywords):
        super().__init__(screen, **keywords)
        self.autowrap = autowrap
        self.center = center
        self._values_cache_for_wrapping = []
        self.widgets_inherit_color = True
        self.color = 'DEFAULT'
        self.lines_placed = False

    def _wrap_message_lines(self, message_lines, line_length):
        lines = []
        if not self.lines_placed:
            for line in message_lines:
                if line.rstrip() == '':
                    lines.append('')
                else:
                    if line.find('\n\t') != -1:
                        user_info, message_text = line.rsplit("\n\t", 1)
                        space = line_length - 1 - len(user_info)
                        name, timestamp = user_info.split('(')
                        message_header = "{}{}({}".format(name.strip(), '.' * space,
                                                          timestamp.strip())
                        lines.append("->{}".format(message_header))
                    else:
                        message_text = line
                    this_line_set = list(map(
                        lambda x: "\t\t\t\t{}".format(x),
                        textwrap.wrap(message_text.rstrip(), line_length - 5)))
                    if this_line_set:
                        lines.extend(this_line_set + [''])
                    else:
                        lines.append('')
        else:
            lines = message_lines
        return lines

    def _set_line_values(self, line, value_indexer):
        try:
            _vl = self.values[value_indexer]
        except IndexError:
            self._set_line_blank(line)
            return False
        except TypeError:
            self._set_line_blank(line)
            return False
        line.value = self.display_value(_vl)
        line.color = _vl.startswith('->') and 'CONTROL' or 'DEFAULT'
        line.hidden = False

    def h_scroll_line_down(self, input):
        self.start_display_at += 1
        if self.scroll_exit and self.height > len(self.values) - self.start_display_at:
            self.editing = False
            self.how_exited = wgwidget.EXITED_DOWN
