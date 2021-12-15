from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QSizePolicy,
    QHBoxLayout,
    QComboBox,
    QSpinBox,
    QPushButton,
)
from components.component import Component


class VariableComponent(Component):
    def _setup(self, description):
        self._setupUI()
        self._setupBE(description)

    def _setupUI(self):
        # create dummy widget to set correct position on layout
        # set sizes of self.verticalLayoutWidget
        self.verticalLayoutWidget = QHBoxLayout(self)
        self.verticalLayoutWidget.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )

        self.bt = QPushButton(self)
        self.bt.setText("⟲")
        self.bt.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.bt.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.bt.clicked.connect(self.update_data)
        self.verticalLayoutWidget.addWidget(self.bt)

        self.variablesCB = QComboBox(self)
        self.variablesCB.addItems(self.variables)
        self.variablesCB.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.verticalLayoutWidget.addWidget(self.variablesCB)

        self.operationsCB = QComboBox(self)
        self.operationsCB.addItems(["=", "+", "-", "*", "/", "%"])
        self.operationsCB.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayoutWidget.addWidget(self.operationsCB)

        self.integer = QSpinBox(self)
        self.integer.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.verticalLayoutWidget.addWidget(self.integer)

    def _setupBE(self, description):
        try:
            self.variablesCB.setCurrentText(
                description.get("varname", self.variables[0])
            )
        except IndexError:
            self.variablesCB.setCurrentText(description.get("varname", ""))
        self.operationsCB.setCurrentText(description.get("operation", "="))
        self.integer.setValue(int(description.get("integer", "0")))

    def update_data(self):
        self.parent().variables = self.mw.variables
        self.variables = self.parent().variables

        self.variablesCB.clear()
        self.variablesCB.addItems(self.variables)

    def validate(self):
        if self.integer.text() == "":
            inte = "0"
        else:
            inte = self.integer.text()

        if (self.operationsCB.currentText() == "/" and inte == "0") or (
            self.operationsCB.currentText() == "%" and inte == "0"
        ):
            return ["devising by zero"]
        else:
            return []

    def returnValue(self):
        if self.integer.text() == "":
            inte = "0"
        else:
            inte = self.integer.text()
        return {
            "type": "variables",
            "varname": self.variablesCB.currentText(),
            "operation": self.operationsCB.currentText(),
            "integer": inte,
        }
