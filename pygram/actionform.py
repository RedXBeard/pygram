import threading
from datetime import datetime

import npyscreen
from DictObject import DictObject
from npyscreen import ActionFormExpanded, ActionForm, wgwidget as widget
from pytg.exceptions import NoResponse, IllegalResponseException
from pytg.utils import coroutine

from pygram import printed, check_version
from pygram.boxtitle import DialogBox, HistoryBox, ChatBox


class PyGramForm(ActionFormExpanded):
    CANCEL_BUTTON_BR_OFFSET = (5, 12)
    OK_BUTTON_TEXT = "QUIT"
    CANCEL_BUTTON_TEXT = "SEND"

    def __init__(self, *args, **kwargs):
        self.TG = kwargs.pop('TG', None)
        self.form_width = 30
        self.receiver_thread = None
        self.full_name = printed(self.TG.sender.get_self())
        self.dialog_list = None
        self.chat_history = None
        self.chat_box = None
        self.editw = 0
        super().__init__(*args, **kwargs)
        self.current_peer = None
        self.version_checked = False

    def set_up_exit_condition_handlers(self):
        super(ActionForm, self).set_up_exit_condition_handlers()
        self.how_exited_handers.update({
            widget.EXITED_ESCAPE: self.find_quit_button
        })

    def find_quit_button(self):
        self.editw = len(self._widgets__) - 1

    def on_ok(self, direct=False):
        if direct:
            self.parentApp.switchForm(None)
        ans = npyscreen.notify_yes_no('Are you sure, you want to quit?')
        if ans:
            self.TG.receiver.stop()
            self.parentApp.switchForm(None)

    def on_screen(self):
        if not self.version_checked and not check_version():
            npyscreen.notify_ok_cancel("New version released please check.")
        self.version_checked = True

    def on_cancel(self):
        """ Message will be send """
        if self.current_peer:
            text = self.chat_box.entry_widget.value.strip()
            if text:
                send_status = self.TG.sender.send_msg(self.current_peer.print_name, text)
                if send_status:
                    self.chat_box.entry_widget.value = ""
                    self.load_history(current_dialog=self.current_peer)
                    self.editw = self._widgets__.index(self.chat_box)
        else:
            npyscreen.notify_ok_cancel('Please select receiver first.')

    def create(self):
        self.dialog_list = self.add(DialogBox, name="Dialog List", scroll_exit=True,
                                    editable=True, max_width=self.form_width, max_height=self._max_physical()[0] - 10)
        self.load_dialogs()

        self.chat_history = self.add(HistoryBox, name="", scroll_exit=True,
                                     editable=True, relx=self.form_width + 2, rely=2,
                                     max_height=self._max_physical()[0] - 10)

        self.chat_box = self.add(ChatBox, name='{}'.format(self.full_name), scroll_exit=True,
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
                    if self.current_peer:
                        if ((self.current_peer.peer_type == 'user' and
                                     self.current_peer.peer_id == msg.sender.peer_id) or
                                (self.current_peer.peer_type == 'chat' and
                                         self.current_peer.peer_id == msg.receiver.peer_id)):
                            self.load_history(trigger_movement=False, current_dialog=self.current_peer)
        except (GeneratorExit, KeyboardInterrupt, TypeError, NoResponse):
            pass

    def trigger_receiver(self):
        try:
            self.TG.receiver.start()
            self.TG.receiver.message(self.message_loop())
        except TypeError:
            npyscreen.notify("Sorry, An error occurred please restart the app :(")
            self.on_ok(direct=True)

    def load_dialogs(self):
        dialog_list = list(reversed(self.TG.sender.dialog_list(retry_connect=True)))

        # Formating display for dialogs
        peer_index = None
        for dial in dialog_list:
            dial.printed = printed(dial)
            if hasattr(self, 'current_peer') and dial == self.current_peer:
                peer_index = dialog_list.index(dial)
            try:
                history = self.TG.sender.history(dial.print_name, 2, 0, retry_connect=True)
                unread = len(list(filter(lambda x: x.unread, history)))
                dial.unread = unread
            except (IllegalResponseException, NoResponse):
                dial.unread = 0
        self.parentApp.dialog_list = dialog_list
        self.dialog_list.values = dialog_list
        self.dialog_list.entry_widget.value = peer_index
        self.dialog_list.update()
        self.find_next_editable()
        self.editw -= 1

    def load_history(self, **keywords):
        current_dialog = keywords.get('current_dialog', None)
        if current_dialog:
            self.current_peer = current_dialog
            self.chat_history.entry_widget.lines_placed = False
            self.chat_history.name = (getattr(current_dialog, 'title', '') or
                                      getattr(current_dialog, 'printed', '') or 'Unknown')

            history = self.TG.sender.history(current_dialog.print_name, 100, 0, retry_connect=True)

            unread = list(filter(lambda x: x.unread, history))
            if unread:
                unread_index = history.index(unread[0])
                history = history[:unread_index] + ["--New Messages--"] + history[unread_index:]
            self.chat_history.values = list(
                filter(lambda x: x,
                       map(lambda x: (
                           isinstance(x, str) and x or '{} ({})\n\t{}'.format(
                               printed(getattr(x, 'from')),
                               datetime.fromtimestamp(getattr(x, 'date', '')),
                               (getattr(x, 'text', '') or
                                getattr(getattr(x, 'media', DictObject()), 'address', '')))),
                           history)))
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
