# encoding: utf-8

from datetime import datetime

import npyscreen
from DictObject import DictObject
from pytg import Telegram

from config import TELEGRAM_CLI_PATH, PUBKEY_FILE

TG = Telegram(telegram=TELEGRAM_CLI_PATH,
              pubkey_file=PUBKEY_FILE)


class PyGramForm(npyscreen.ActionForm):
    form_width = 30

    def on_ok(self):
        self.parentApp.switchForm(None)

    def create(self):
        self.dialog_list = self.add(npyscreen.BoxTitle, name="Dialog List", scroll_exit=True,
                                    editable=True, max_width=self.form_width)
        self.dialog_list.values = list(map(lambda x: x.print_name, self.parentApp.dialog_list))
        self.dialog_list.add_handlers({'^D': self.load_history})

        self.chat_history = self.add(npyscreen.BoxTitle, name="", scroll_exit=True,
                                     editable=False, relx=self.form_width + 2, rely=2)

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
                           TG.sender.history(printed_name, 10, 0))))
            self.parentApp.fill_history()

        # Force movement to history box
        self.find_next_editable()
        # Coused of force editable widget index also should be updated
        self.editw += 1


class PyGramApp(npyscreen.NPSAppManaged):
    dialog_list = []
    contacts_list = []

    def onStart(self):
        self.dialog_list = TG.sender.dialog_list()
        self.contacts_list = TG.sender.contacts_list()
        self.addForm('MAIN', PyGramForm, name='Welcome PyGram')

    def onCleanExit(self):
        npyscreen.notify_wait("Goodbye!")

    def fill_history(self):
        # Switch forms.  NB. Do *not* call the .edit() method directly (which
        # would lead to a memory leak and ultimately a recursion error).
        # Instead, use the method .switchForm to change forms.

        # By default the application keeps track of every form visited.
        # There's no harm in this, but we don't need it so:
        self.resetHistory()


if __name__ == "__main__":
    PyGramApp().run()
