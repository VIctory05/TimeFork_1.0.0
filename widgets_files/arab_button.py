from PyQt5.QtWidgets import QPushButton


class ArabButton(QPushButton):
    def __init__(
        self, parent, conected_widget, function_to_parent_on_close=lambda: None
    ):
        self.conected_widget = conected_widget
        super(ArabButton, self).__init__(parent)
        self.clicked.connect(self.AlahAacbar)
        self.setText("-")
        self.conected_widget.get_arab = lambda: self
        self.on_close_function = function_to_parent_on_close

    def AlahAacbar(self):
        self.on_close_function()
        self.conected_widget.setParent(None)
        self.setParent(None)

# ArabButton это пасхалка! Это кнопка, которая убирает компонент.
