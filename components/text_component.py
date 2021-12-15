from PyQt5 import QtCore
from PyQt5.QtWidgets import QTextEdit, QSizePolicy, QVBoxLayout
from components.component import Component


class TextComponent(Component):
    def _setup(self, description):
        self._setupUI()
        self._setupBE(description)

    def _setupUI(self):
        # create dummy widget to set correct position on layout
        # set sizes of self.verticalLayoutWidget
        self.verticalLayoutWidget = QVBoxLayout(self)
        self.verticalLayoutWidget.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )

        self.textField = QTextEdit(self)
        self.textField.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.verticalLayoutWidget.addWidget(self.textField)

    def _setupBE(self, description):
        self.textField.setText(description.get("data", ""))

    def validate(self):
        return []

    def returnValue(self):
        return {"type": "text", "data": self.textField.toPlainText()}
