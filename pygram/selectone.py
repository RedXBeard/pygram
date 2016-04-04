# encoding: utf-8

from npyscreen import SelectOne
from pygram.checkbox import CustomRoundCheckBox


class CustomSelectOne(SelectOne):
    _contained_widgets = CustomRoundCheckBox
