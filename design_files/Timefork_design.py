from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QToolBar,
    QLineEdit,
    QVBoxLayout,
    QTabWidget,
    QSizePolicy,
    QTreeWidget,
    QShortcut,
    QMenuBar,
    QMenu,
    QAction,
    QStyle,
)


class TimeForkDesign:
    def _setupUi(self, Form):  # setup UI

        self.main_tool_box = QToolBar("tree")
        self.main_tool_box.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.main_tool_box)

        Form.setObjectName("Form")  # set name of window
        Form.resize(1070, 808)  # set size of window

        # create lineEdit to edit quest's author name
        self.authotField = QLineEdit()
        self.main_tool_box.addWidget(self.authotField)

        # create vertical layout to storage Timefork_settings widget
        self.verticalLayoutWidget = QVBoxLayout(
            Form
        )  # create dummy widget to set correct position on layout  # set sizes of self.verticalLayoutWidget
        self.verticalLayoutWidget.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )
        self.settings_storage = QTabWidget(self)
        # create layout in self.verticalLayoutWidget
        self.settings_storage.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self.verticalLayoutWidget.addWidget(
            self.settings_storage,
            alignment=QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter,
        )
        self.setCentralWidget(self.settings_storage)
        self.settings_storage.setTabsClosable(True)

        self.tree = QTreeWidget()  # create QTreeWidget to visualize quest's graph
        self.tree.setColumnCount(1)  # set number of self.tree's columns
        self.tree.setHeaderLabels([""])  # set header labels of self.tree
        self.tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.main_tool_box.addWidget(self.tree)

        self.saveSK = QShortcut(
            QKeySequence("Ctrl+S"), self
        )  # creating shortcut on Ctrl+S

    def _menuBar(self):
        menuBar = QMenuBar(self)

        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

        toolsMenu = QMenu("&Tools", self)
        menuBar.addMenu(toolsMenu)
        toolsMenu.addAction(self.variablesAction)
        toolsMenu.addAction(self.helpAction)

        self.setMenuBar(menuBar)

    def _createToolBars(self):
        fileToolBar = self.addToolBar("File")
        fileToolBar.addAction(self.newAction)
        fileToolBar.addAction(self.openAction)
        fileToolBar.addAction(self.saveAction)

        toolsTollBar = self.addToolBar("Tools")
        toolsTollBar.addAction(self.variablesAction)
        toolsTollBar.addAction(self.runAction)

    def _createActions(self):
        # Creating action using the first constructor
        self.newAction = QAction(
            self.style().standardIcon(QStyle.SP_FileDialogNewFolder), "&New...", self
        )
        self.openAction = QAction(
            self.style().standardIcon(QStyle.SP_DirOpenIcon), "&Open...", self
        )
        self.saveAction = QAction(
            self.style().standardIcon(QStyle.SP_DialogSaveButton), "&Save", self
        )
        self.exitAction = QAction(
            self.style().standardIcon(QStyle.SP_MessageBoxCritical), "&Exit", self
        )
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("C&ut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)
        self.variablesAction = QAction(
            self.style().standardIcon(QStyle.SP_ArrowDown), "&Variables", self
        )
        self.copyAddressAction = QAction("&Copy Name")
        self.helpAction = QAction("&Help...")
        self.runAction = QAction(
            self.style().standardIcon(QStyle.SP_ArrowForward), "&Run", self
        )
