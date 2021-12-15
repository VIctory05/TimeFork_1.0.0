from PyQt5 import QtWidgets

from widgets_files.arab_button import ArabButton


class Component(QtWidgets.QWidget):
    def __init__(self, parent, description, variables, mw=None):
        super(Component, self).__init__(parent)
        self.variables = variables
        self.mw = mw
        self.description = description
        self._setup(description)

        self.arab = ArabButton(
            self.parent(),
            self,
            function_to_parent_on_close=lambda: self.parent().components.remove(self),
        )

    def _setup(self, description):
        pass
