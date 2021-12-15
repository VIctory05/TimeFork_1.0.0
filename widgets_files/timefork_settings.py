from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QLabel,
    QLineEdit,
    QGridLayout,
    QComboBox,
    QFrame,
    QMessageBox,
)

from components.choice_component import ChoiceComponent
from components.goto_component import GotoComponent
from components.text_component import TextComponent
from components.variables_component import VariableComponent
from widgets_files.id_QLineEdit import IdQLineEdit

COMPONENTS = {
    "text": TextComponent,
    "goto": GotoComponent,
    "variables": VariableComponent,
    "choice": ChoiceComponent,
}


class TimeforkSettingsDesign:
    def _setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = self
        self.centralwidget.setObjectName("centralwidget")
        self.main_layout = QGridLayout(self.centralwidget)
        self.nameLabel = QLabel(self.centralwidget)
        self.main_layout.addWidget(self.nameLabel)
        self.nameLabel.setObjectName("nameLabel")
        self.startWay = QLineEdit(self.centralwidget)
        self.startWay.setPlaceholderText("Name...")
        self.startWay.setObjectName("startWay")
        self.main_layout.addWidget(self.startWay, 1, 0)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        self.main_layout.addWidget(line, 2, 0)

        self.addcomponent = QComboBox(self.centralwidget)
        self.addcomponent.addItem("")
        self.main_layout.addWidget(self.addcomponent)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _setupSignals(self):
        for obj in COMPONENTS.keys():
            self.addcomponent.addItem(obj)

        self.addcomponent.currentTextChanged.connect(self.add_new)


class TimeforkSettings(QtWidgets.QWidget, TimeforkSettingsDesign):
    def __init__(
        self,
        id_list,
        description: list,
        variables: list,
        counter: int,
        main_widget=None,
    ):
        super(TimeforkSettings, self).__init__()
        self._setupUi(self)
        self._setupSignals()
        self.lineEdits: list[IdQLineEdit] = []

        self.components = []
        self.id = id_list[-1]
        self.normal_way = id_list
        self.description = description
        print(self.description[self.id])
        self.name = self.description[self.id]["name"]
        self.startWay.setText(self.name)
        self.nameLabel.setText(self.name)
        self.variables = variables
        self.counter = counter
        self.components_counter = 4

        self.main_widget = main_widget

        self.allinBlanc()

    def validate(self):
        arr = []
        for component in self.components:
            arr = arr + component.validate()
        return arr

    def allinConsole(self):
        try:
            self.parent().parent().parent().description_data[self.id] = {
                "name": self.name,
                "components": [
                    component.returnValue() for component in self.components
                ],
            }
        except Exception:
            pass
        return {
            "name": self.name,
            "components": [component.returnValue() for component in self.components],
        }

    def add_new(self):
        if self.addcomponent.currentText():
            if not len(self.components) or self.components[-1].description.get(
                "type"
            ) not in {
                "goto",
                "choice",
            }:
                self.add_component({"type": self.addcomponent.currentText()})
                self.addcomponent.setCurrentIndex(0)
            else:
                QMessageBox.warning(
                    self,
                    "Предупреждение",
                    "Нельзя добавлять компоненты после goto и choice",
                )

    def allinBlanc(self):
        for i in self.description[self.id]["components"]:
            self.add_component(i)

    def add_component(self, component):
        nc = COMPONENTS[component["type"]](
            self, component, self.variables, mw=self.main_widget
        )
        self.components.append(nc)
        self.main_layout.addWidget(nc, self.components_counter, 0)
        self.main_layout.addWidget(nc.get_arab(), self.components_counter, 1)
        self.components_counter += 1
        print(self.allinConsole())
