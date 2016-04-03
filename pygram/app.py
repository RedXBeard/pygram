from npyscreen import NPSAppManaged
from pytg import Telegram

from pygram.actionform import PyGramForm
from pygram.config import TELEGRAM_CLI_PATH, PUBKEY_FILE

TG = Telegram(telegram=TELEGRAM_CLI_PATH,
              pubkey_file=PUBKEY_FILE)


class PyGramApp(NPSAppManaged):
    dialog_list = []
    contacts_list = []

    def onStart(self):
        self.dialog_list = TG.sender.dialog_list(retry_connect=True)
        self.contacts_list = TG.sender.contacts_list()
        self.addForm('MAIN', PyGramForm, name='Welcome PyGram', TG=TG)

    def fill_history(self):
        self.resetHistory()
