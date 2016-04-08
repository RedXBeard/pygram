from npyscreen.muNewMenu import MenuItem

from pygram import printed


class CustomMenuItem(MenuItem):
    def __init__(self, obj=None, onSelect=None, shortcut=None, document=None, arguments=None, keywords=None):
        text = obj and printed(obj) or ''
        super().__init__(text, onSelect, shortcut, document, arguments, keywords)
        self.obj = obj
