# encoding: utf-8

import npyscreen
from pytg import Telegram

from config import TELEGRAM_CLI_PATH, PUBKEY_FILE

TG = Telegram(telegram=TELEGRAM_CLI_PATH,
              pubkey_file=PUBKEY_FILE)


class PyGramForm(npyscreen.Form):
    form_width = 30

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def create(self):
        max_width_ondialog = self.form_width - 8
        self.dialog_list = self.add(npyscreen.BoxTitle, name="Dialog List", scroll_exit=True,
                                    editable=True, max_width=self.form_width)
        self.dialog_list.values = list(map(
            lambda x: (len(x.print_name) > max_width_ondialog and
                       x.print_name[:max_width_ondialog] + '...' or
                       x.print_name),
            TG.sender.dialog_list()))


class PyGramApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', PyGramForm, name='Welcome PyGram')


if __name__ == "__main__":
    PyGramApp().run()
