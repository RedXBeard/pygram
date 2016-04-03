# encoding: utf-8

import logging
import threading
from datetime import datetime

import npyscreen
from DictObject import DictObject
from npyscreen import wgwidget as widget
from pytg import Telegram
from pytg.exceptions import NoResponse
from pytg.utils import coroutine

from pygram.boxtitle import DialogBox, HistoryBox, ChatBox
from pygram.config import TELEGRAM_CLI_PATH, PUBKEY_FILE

TG = Telegram(telegram=TELEGRAM_CLI_PATH,
              pubkey_file=PUBKEY_FILE)
logger = logging.getLogger("main")


class PyGramForm(npyscreen.ActionFormExpanded):
    CANCEL_BUTTON_BR_OFFSET = (5, 12)
    OK_BUTTON_TEXT = "QUIT"
    CANCEL_BUTTON_TEXT = "SEND"
    FULL_NAME = '{} {}'.format(TG.sender.get_self().first_name, TG.sender.get_self().last_name)

    def __init__(self, *args, **kwargs):
        self.form_width = 30
        self.receiver_thread = None
        super().__init__(*args, **kwargs)
        self.current_peer = None

    def on_ok(self, direct=False):
        if direct:
            self.parentApp.switchForm(None)
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
                                 editable=True, max_height=5)

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
        except (GeneratorExit, KeyboardInterrupt, TypeError, NoResponse):
            pass

    def trigger_receiver(self, *args, **keywords):
        try:
            TG.receiver.start()
            TG.receiver.message(self.message_loop())
        except TypeError:
            npyscreen.notify("Sorry, An error occurred please restart the app :(")
            self.on_ok(direct=True)

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
            # Force movement to chat box
            for wid in self._widgets__:
                if wid == self.chat_box:
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
    # from run import main
    logging.basicConfig(filename="./log/pygram-{}.log".format(datetime.now().date()))
    # sys.exit(main())
    PyGramApp().run()
