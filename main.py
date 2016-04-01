# encoding: utf-8

import logging
import textwrap
import threading
from datetime import datetime

import npyscreen
from DictObject import DictObject
from npyscreen import Textfield
from npyscreen import wgwidget as widget
from pytg import Telegram
from pytg.exceptions import NoResponse
from pytg.utils import coroutine

from config import TELEGRAM_CLI_PATH, PUBKEY_FILE

TG = Telegram(telegram=TELEGRAM_CLI_PATH,
              pubkey_file=PUBKEY_FILE)
logger = logging.getLogger("main")


class ChatBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Textfield


class CustomPager(npyscreen.Pager):
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
            self.how_exited = widget.EXITED_DOWN


class HistoryBox(npyscreen.BoxTitle):
    _contained_widget = CustomPager


class CustomRoundCheckBox(npyscreen.RoundCheckBox):
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


class CustomSelectOne(npyscreen.SelectOne):
    _contained_widgets = CustomRoundCheckBox


class DialogBox(npyscreen.BoxTitle):
    _contained_widget = CustomSelectOne


class PyGramForm(npyscreen.ActionFormExpanded):
    CANCEL_BUTTON_BR_OFFSET = (5, 12)
    OK_BUTTON_TEXT = "QUIT"
    CANCEL_BUTTON_TEXT = "SEND"
    FULL_NAME = '{} {}'.format(TG.sender.get_self().first_name, TG.sender.get_self().last_name)

    def __init__(self, *args, **kwargs):
        self.form_width = 30
        super().__init__(*args, **kwargs)
        self.current_peer = None

    def on_ok(self):
        ans = npyscreen.notify_yes_no('Are you sure, you want to quit?')
        if ans:
            TG.receiver.stop()
            self.parentApp.switchForm(None)

    def on_cancel(self):
        """ Message will be send """
        if self.dialog_list.entry_widget and self.dialog_list.entry_widget.value:
            selected_index = self.dialog_list.entry_widget.value[0]
            dialog_name = self.dialog_list.values[selected_index]
            text = self.chat_box.entry_widget.value.strip()
            if text:
                send_status = TG.sender.send_msg(dialog_name, text)
                if send_status:
                    self.chat_box.entry_widget.value = ""
                    self.load_history()
                    self.dialog_list.entry_widget.value = self.dialog_list.values.index(self.current_peer.print_name)
                    self.editw = self._widgets__.index(self.chat_box)
        else:
            npyscreen.notify_ok_cancel('Please select receiver first.')

    def create(self):
        self.dialog_list = self.add(DialogBox, name="Dialog List", scroll_exit=True,
                                    editable=True, max_width=self.form_width, max_height=self._max_physical()[0] - 10)
        self.load_dialogs()

        self.dialog_list.add_handlers({'^D': self.load_history})

        self.chat_history = self.add(HistoryBox, name="", scroll_exit=True,
                                     editable=True, relx=self.form_width + 2, rely=2,
                                     max_height=self._max_physical()[0] - 10)

        self.chat_box = self.add(ChatBox, name='{}'.format(self.FULL_NAME), scroll_exit=True,
                                 editable=True, max_height=5, contained_widget_arguments={'name': ' '})

        self.start_receiver()

    def start_receiver(self):
        self.receiver_thread = threading.Thread(target=self.trigger_receiver)
        self.receiver_thread.daemon = True
        self.receiver_thread.start()

    @coroutine
    def message_loop(self):
        try:
            while True:
                msg = (yield)
                if msg.event != "message" or msg.own:
                    continue
                else:
                    self.load_dialogs()
                    if self.dialog_list.entry_widget and self.dialog_list.entry_widget.value:
                        selected_index = self.dialog_list.entry_widget.value[0]
                        printed_name = self.dialog_list.values[selected_index]
                        current_dialog = list(filter(lambda x: x.print_name == printed_name,
                                                     self.parentApp.dialog_list))[0]
                        if ((current_dialog.peer_type == 'user' and current_dialog.peer_id == msg.sender.peer_id) or
                                (current_dialog.peer_type == 'chat' and
                                         current_dialog.peer_id == msg.receiver.peer_id)):
                            self.load_history(trigger_movement=False)
        except (GeneratorExit, KeyboardInterrupt, NoResponse):
            pass

    def trigger_receiver(self, *args, **keywords):
        TG.receiver.start()
        TG.receiver.message(self.message_loop())

    def load_dialogs(self, *args, **keywords):
        dialog_list = TG.sender.dialog_list(retry_connect=True)
        self.parentApp.dialog_list = dialog_list
        self.dialog_list.values = list(map(lambda x: x.print_name, self.parentApp.dialog_list))

    def load_history(self, *args, **keywords):
        selected_index = self.dialog_list.entry_widget.value[0]
        printed_name = self.dialog_list.values[selected_index]
        selected_dialog = list(filter(
            lambda x: x.print_name == printed_name, self.parentApp.dialog_list))
        if selected_dialog:
            self.current_peer = selected_dialog[0]
            self.chat_history.entry_widget.lines_placed = False
            self.chat_history.name = (getattr(selected_dialog[0], 'title', None) or
                                      "{} {}".format(getattr(selected_dialog[0], 'first_name', ''),
                                                     getattr(selected_dialog[0], 'last_name', '')))

            self.chat_history.values = list(
                filter(lambda x: x,
                       map(lambda x: (
                           '{} {} ({})\n\t{}'.format(getattr(getattr(x, 'from'), 'first_name', ''),
                                                     getattr(getattr(x, 'from'), 'last_name', ''),
                                                     datetime.fromtimestamp(getattr(x, 'date', '')),
                                                     (getattr(x, 'text', '') or
                                                      getattr(getattr(x, 'media', DictObject()), 'address', '')))),
                           TG.sender.history(printed_name, 100, 0, retry_connect=True))))
            self.parentApp.fill_history()
            self.find_next_editable()
            self.editw -= 1
            self.chat_history.entry_widget.lines_placed = True
            self.chat_history.update()
            self.chat_history.entry_widget.h_show_end(None)
            self.find_next_editable()
            self.editw -= 1

        if keywords.get('trigger_movement', True):
            # Force movement to history box
            self.editw = 0
            for wid in self._widgets__:
                if wid == self.chat_box:
                    wid.how_exited = widget.EXITED_DOWN
                    self.editw = self._widgets__.index(wid)
                    self._widgets__[self.editw].editing = True
                    self._widgets__[self.editw].edit()
                    self._widgets__[self.editw].display()
                    break
                wid.editing = False
                wid.how_exited = widget.EXITED_DOWN
                self.handle_exiting_widgets(wid.how_exited)
        self.load_dialogs()
        self.dialog_list.update()


class PyGramApp(npyscreen.NPSAppManaged):
    dialog_list = []
    contacts_list = []

    def onStart(self):
        self.dialog_list = TG.sender.dialog_list(retry_connect=True)
        self.contacts_list = TG.sender.contacts_list()
        self.addForm('MAIN', PyGramForm, name='Welcome PyGram')

    def fill_history(self):
        self.resetHistory()


if __name__ == "__main__":
    logging.basicConfig(filename="./log/pygram-{}.log".format(datetime.now().date()))
    PyGramApp().run()
