from PyQt5.QtWidgets import QLineEdit


class IdQLineEdit(QLineEdit):
    def __init__(self, parent, id):
        self.id = id
        super(IdQLineEdit, self).__init__(parent)
