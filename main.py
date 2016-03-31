# encoding: utf-8

from datetime import datetime
import logging

import npyscreen
from DictObject import DictObject
from pytg import Telegram

from config import TELEGRAM_CLI_PATH, PUBKEY_FILE

TG = Telegram(telegram=TELEGRAM_CLI_PATH,
              pubkey_file=PUBKEY_FILE)


class ChatBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.Textfield


class PyGramForm(npyscreen.ActionForm):
    form_width = 30
    full_name = '{} {}'.format(TG.sender.get_self().first_name, TG.sender.get_self().last_name)

    def on_ok(self):
        self.parentApp.switchForm(None)

    def create(self):
        print(self._max_physical())
        self.dialog_list = self.add(npyscreen.BoxTitle, name="Dialog List", scroll_exit=True,
                                    editable=True, max_width=self.form_width, max_height=self._max_physical()[0] - 10)
        self.dialog_list.values = list(map(lambda x: x.print_name, self.parentApp.dialog_list))

        self.dialog_list.add_handlers({'^D': self.load_history})

        self.chat_history = self.add(npyscreen.BoxTitle, name="", scroll_exit=True,
                                     editable=True, relx=self.form_width + 2, rely=2,
                                     max_height=self._max_physical()[0] - 10)

        self.chat_box = self.add(ChatBox, name='{}'.format(self.full_name), scroll_exit=True,
                                 editable=True, max_height=5, contained_widget_arguments={'name': ' '})

    def load_history(self, *args, **keywords):
        selected_index = self.dialog_list.entry_widget.value
        printed_name = self.dialog_list.values[selected_index]
        selected_dialog = list(filter(
            lambda x: x.print_name == printed_name, self.parentApp.dialog_list))
        if selected_dialog:
            self.chat_history.name = (getattr(selected_dialog[0], 'title', None) or
                                      "{} {}".format(getattr(selected_dialog[0], 'first_name', ''),
                                                     getattr(selected_dialog[0], 'last_name', '')))

            self.chat_history.values = list(
                filter(lambda x: x,
                       map(lambda x: (
                           '{} {} ({}) -> {}'.format(getattr(getattr(x, 'from'), 'first_name', ''),
                                                     getattr(getattr(x, 'from'), 'last_name', ''),
                                                     datetime.fromtimestamp(getattr(x, 'date', '')),
                                                     (getattr(x, 'text', '') or
                                                      getattr(getattr(x, 'media', DictObject()), 'address', '')))),
                           TG.sender.history(printed_name, 100, 0, retry_connect=True))))
            self.parentApp.fill_history()

        # Force movement to history box
        self.find_next_editable()
        # Coused of force editable widget index also should be updated
        self.editw = 0


class PyGramApp(npyscreen.NPSAppManaged):
    dialog_list = []
    contacts_list = []

    def onStart(self):
        self.dialog_list = reversed(TG.sender.dialog_list(retry_connect=True))
        self.contacts_list = TG.sender.contacts_list()
        self.addForm('MAIN', PyGramForm, name='Welcome PyGram')

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")

    def fill_history(self):
        self.resetHistory()

if __name__ == "__main__":
    logging.basicConfig(filename="./log/pygram-{}.log".format(datetime.now()))
    PyGramApp().run()
