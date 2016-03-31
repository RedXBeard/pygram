# encoding: utf-8

import logging
import textwrap
import threading
from datetime import datetime

import npyscreen
from DictObject import DictObject
from npyscreen import wgwidget as widget
from pytg import Telegram
from pytg.utils import coroutine

from config import TELEGRAM_CLI_PATH, PUBKEY_FILE

TG = Telegram(telegram=TELEGRAM_CLI_PATH,
              pubkey_file=PUBKEY_FILE)


def message_loop():
    try:
        while True:
            msg = (yield)
            if msg.event != "message":
                continue
            if msg.own:
                continue
            if msg.text is None:
                continue
            else:
                print("({}) {} {} -> {}".format(msg.receiver.title, msg.sender.first_name, msg.sender.last_name,
                                                msg.text.strip()))
    except GeneratorExit:
        pass
    except KeyboardInterrupt:
        pass
    else:
        pass

class SendButton(npyscreen.MiniButtonPress):
    def whenPressed(self):
        pass


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

    def display_value(self, vl):
        try:
            return self.safe_string(str(vl))
        except ReferenceError:
            return "**REFERENCE ERROR**"

    def h_scroll_line_down(self, input):
        self.start_display_at += 1
        if self.scroll_exit and (self.start_display_at >= len(self.values) - self.start_display_at + 1 or
                                         self.height >= len(self.values) - self.start_display_at + 1):
            self.editing = False
            self.how_exited = widget.EXITED_DOWN


class HistoryBox(npyscreen.BoxTitle):
    _contained_widget = CustomPager


class PyGramForm(npyscreen.ActionFormExpanded):
    CANCEL_BUTTON_BR_OFFSET = (5, 12)
    OK_BUTTON_TEXT = "QUIT"
    CANCEL_BUTTON_TEXT = "SEND"
    form_width = 30
    full_name = '{} {}'.format(TG.sender.get_self().first_name, TG.sender.get_self().last_name)

    def on_ok(self):
        ans = npyscreen.notify_yes_no('Are you sure, you want to quit?')
        if ans:
            TG.receiver.stop()
            self.parentApp.switchForm(None)

    def on_cancel(self):
        """ Message will be send """
        if self.dialog_list.entry_widget and self.dialog_list.entry_widget.value:
            selected_index = self.dialog_list.entry_widget.value
            dialog_name = self.dialog_list.values[selected_index]
            text = self.chat_box.entry_widget.value.strip()
            if text:
                send_status = TG.sender.send_msg(dialog_name, text)
                if send_status:
                    self.chat_box.entry_widget.value = ""
                    self.load_history()
        else:
            npyscreen.notify_ok_cancel('Please select receiver first.')

    def create(self):
        self.dialog_list = self.add(npyscreen.BoxTitle, name="Dialog List", scroll_exit=True,
                                    editable=True, max_width=self.form_width, max_height=self._max_physical()[0] - 10)
        self.load_dialogs()

        self.dialog_list.add_handlers({'^D': self.load_history})

        self.chat_history = self.add(HistoryBox, name="", scroll_exit=True,
                                     editable=True, relx=self.form_width + 2, rely=2,
                                     max_height=self._max_physical()[0] - 10)

        self.chat_box = self.add(ChatBox, name='{}'.format(self.full_name), scroll_exit=True,
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
                    self.chat_box.entry_widget.value = msg.text.strip()
                    self.chat_box.update()
                    self.find_next_editable()
                    self.editw = 0
                    self.load_dialogs()
        except (GeneratorExit, KeyboardInterrupt):
            pass
        else:
            pass

    def trigger_receiver(self, *args, **keywords):
        TG.receiver.start()
        TG.receiver.message(self.message_loop())

    def load_dialogs(self, *args, **keywords):
        dialog_list = TG.sender.dialog_list(retry_connect=True)
        self.parentApp.dialog_list = dialog_list
        self.dialog_list.values = list(map(lambda x: x.print_name, self.parentApp.dialog_list))

    def load_history(self, *args, **keywords):
        selected_index = self.dialog_list.entry_widget.value
        printed_name = self.dialog_list.values[selected_index]
        selected_dialog = list(filter(
            lambda x: x.print_name == printed_name, self.parentApp.dialog_list))
        if selected_dialog:
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
            self.chat_history.entry_widget.lines_placed = True

        # Force movement to history box
        self.find_next_editable()
        self.chat_history.entry_widget.h_show_end(None)
        self.find_next_editable()
        self.editw = 0
        for wid in self._widgets__:
            if wid == self.chat_box:
                wid.how_exited = widget.EXITED_DOWN
                self.editw = self._widgets__.index(wid)
                self._widgets__[self.editw].edit()
                self._widgets__[self.editw].display()
                break
            wid.how_exited = widget.EXITED_DOWN
            self.handle_exiting_widgets(wid.how_exited)
            self.editw += 1
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
    logging.basicConfig(filename="./log/pygram-{}.log".format(datetime.now()))
    PyGramApp().run()
