from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QLineEdit,
    QVBoxLayout,
)
from components.component import Component


class GotoComponent(Component):
    def _setup(self, description):
        self._setupUI()
        self._setupBE(description)
        self.description = description

    def _setupUI(self):
        # create dummy widget to set correct position on layout
        # set sizes of self.verticalLayoutWidget
        self.verticalLayoutWidget = QVBoxLayout(self)
        self.verticalLayoutWidget.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )

        self.textField = QLineEdit(self)
        self.textField.setPlaceholderText("Go to...")

        self.verticalLayoutWidget.addWidget(self.textField)

    def _setupBE(self, description):
        self.textField.setText(description.get("data", ""))

    def validate(self):
        if self.textField.text() in [
            i.get("name", "☭") for i in self.mw.description_data
        ]:
            return []
        else:
            return [f'"{self.textField.text()}" don\'t exist']

    def returnValue(self):
        return {"type": "goto", "data": self.textField.text()}
