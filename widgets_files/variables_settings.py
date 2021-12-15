from PyQt5 import QtCore
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import (
    QLineEdit,
    QGridLayout,
    QPushButton,
    QTableWidget,
    QWidget,
    QDialog,
    QTableWidgetItem,
    QAction,
    QMenu,
    QStyle,
)
from components.goto_component import GotoComponent
from components.text_component import TextComponent

COMPONENTS = {"text": TextComponent, "goto": GotoComponent}


class VariablesSettingsDesign:
    def _setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        self.centralwidget = self
        self.centralwidget.setObjectName("centralwidget")
        self.main_layout = QGridLayout(self.centralwidget)

        self.variables = QTableWidget(self)
        self.variables.setColumnCount(1)
        header = self.variables.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.variables.setHorizontalHeader(header)
        self.variables.horizontalHeader().hide()
        self.variables.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.main_layout.addWidget(self.variables, 0, 0, 3, 3)

        self.minusButton = QPushButton(self)
        self.minusButton.setText("-")
        self.main_layout.addWidget(self.minusButton, 4, 0)

        self.addButton = QPushButton(self)
        self.addButton.setText("+")
        self.main_layout.addWidget(self.addButton, 4, 1)

        self.saveButton = QPushButton(self)
        self.saveButton.setText("save...")
        self.main_layout.addWidget(self.saveButton, 4, 2)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def _setupActions(self):
        self.removeAction = QAction(
            self.style().standardIcon(QStyle.SP_TrashIcon), "&Delete", self
        )

    def _setupSignals(self):
        self.addButton.clicked.connect(self.newVariable)
        self.saveButton.clicked.connect(self.save)
        self.minusButton.clicked.connect(self.deleteRow)

        self.variables.customContextMenuRequested.connect(self.variables_menu)

    def _connectActions(self):
        self.removeAction.triggered.connect(self.deleteRow)


class VariablesSettings(QDialog, VariablesSettingsDesign):
    def __init__(self, variables: list, parent=None):
        super(VariablesSettings, self).__init__(parent)
        self._setupUi(self)
        self._setupActions()
        self._connectActions()
        self._setupSignals()
        self.counter = 0
        self.data = variables
        self.allinBlanc()

    def newVariable(self):
        wd = QWidget()
        ln = QLineEdit(wd)
        self.variables.setRowCount(self.counter)
        self.variables.setCellWidget(self.counter, 0, ln)
        self.counter += 1

    def variables_menu(self):
        menu = QMenu()
        menu.addAction(self.removeAction)
        menu.exec_(QtGui.QCursor.pos())

    def allinBlanc(self):
        self.variables.setRowCount(len(self.data))

        # Column count
        self.variables.setColumnCount(1)
        for value in self.data:
            self.variables.setItem(self.counter, 0, QTableWidgetItem(value))
            self.counter += 1

    def allinConsole(self):
        print(*[self.variables.item(i, 0).text() for i in range(self.counter - 1)])
        return [self.variables.item(i, 0).text() for i in range(self.counter - 1)]

    def deleteRow(self):
        self.variables.removeRow(self.variables.currentRow())
        self.counter -= 1

    def save(self):
        print(self.allinConsole())
        self.parent().variables = self.allinConsole()
        self.close()
