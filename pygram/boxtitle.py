# encoding: utf-8

from npyscreen import BoxTitle
from npyscreen import Textfield
from pygram.pager import CustomPager
from pygram.selectone import CustomSelectOne


class DialogBox(BoxTitle):
    _contained_widget = CustomSelectOne


class HistoryBox(BoxTitle):
    _contained_widget = CustomPager


class ChatBox(BoxTitle):
    _contained_widget = Textfield
