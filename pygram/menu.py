from npyscreen.muNewMenu import NewMenu

from pygram.menuitem import CustomMenuItem


class CustomMenu(NewMenu):
    def addItemsFromList(self, item_list):
        for l in item_list:
            if isinstance(l, CustomMenuItem):
                self.addNewSubmenu(*l)
            else:
                self.addItem(*l)

    def addItem(self, *args, **keywords):
        _itm = CustomMenuItem(*args, **keywords)
        self._menuList.append(_itm)
