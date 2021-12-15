import sys  # import sys for ability of closing programme
import os
from functools import reduce  # import reduce for some recurse functions
import operator  # import operator for some recurse functions
import json  # import json for interaction with .json files
import pyperclip

from PyQt5 import (
    QtCore,
)  # import QtCore for some useful functions to interact with QWidgets
from PyQt5.QtWidgets import (
    QApplication,  # import QtWidgets.QApplication for launch rockets to USA
    QFileDialog,  # import QtWidgets.QFileDialog to use already working file chooser system
    QMainWindow,
    QMenu,
    QMessageBox,
    QToolBar,
)
from PyQt5 import QtGui

from widgets_files.timefork_settings import (
    TimeforkSettings,
)  # import custom widgets from timeforkSettings.py
from design_files.Timefork_design import TimeForkDesign
from widgets_files.id_QTreeWidgetItem import IdQTreeWidgetItem
from interpretare import InterPretate

from widgets_files.variables_settings import VariablesSettings

from widgets_files.help import Help_Dialog
from database import LastChange, DB_PATH

# for changing quest's graph's vertex

ROOT = os.path.abspath(__file__)
if ROOT.endswith(".pyc"):
    ROOT = "\\".join(ROOT.split("\\")[:-3])
else:
    ROOT = "\\".join(ROOT.split("\\")[:-1])


class TimeFork(QMainWindow, TimeForkDesign):  # create main class
    def __init__(self):  # special method __init__ run when we initialize widget
        super().__init__()  # initialize QWidget
        self._setupUi(self)  # setup UI
        self._createActions()  # create Actions
        self._connectActions()  # connect Actions
        self._menuBar()  # creating menu bar
        self._createToolBars()  # creating Tool bars
        self._setupSignals()  # setup signals

        self.counter = 0  # init counter for correct ids
        # init string with name of current file to read and save quest
        self.current_file = ""
        db = LastChange(DB_PATH)
        obj = db.filter()
        if obj is not None:
            if not os.path.isfile(obj.file_path):
                db.api.execute("DELETE FROM lastchange WHERE id=?", obj.id)
                db.api.commit()
            else:
                self.current_file = obj.file_path
                self.change_data()

        # init list of opened tabs to know what tabs are opened at the moment
        self.opened_tabs = []
        self.current_item_settings = None

        self.clicked_pos = QtCore.QPoint(0, 0)  # init variable to know where user click

        self.current_index = -1  # init variable to know what tab is opened now

        (
            author,  # author name
            self.counter,  # set counter on position from file
            self.variables,  # load quest variables names
            self.guide_data,  # load "road map" of quest
            self.description_data,  # load description of quest
        ) = self.load_json()  # init main variables

        self.authotField.setText(author)  # set author name on it place

        self.fill_widget(self.tree, self.guide_data)  # fill guide to tree widget

        file = os.path.join(ROOT, "first_run.txt")
        if os.path.isfile(file):
            with open(file, encoding="utf-8") as f:
                data = f.read()
                if data == "first run":
                    self.help_dialog()
            os.remove(file)

    def _setupSignals(self):  # setup Signals
        self.tree.clicked.connect(self.change_vertex)
        self.tree.customContextMenuRequested.connect(self.treeMenu)

        self.settings_storage.currentChanged.connect(lambda x: self.saveFile())
        self.settings_storage.tabCloseRequested.connect(
            lambda index: self.close_tab(index)
        )

        self.saveSK.activated.connect(self.saveFile)

    def _connectActions(self):
        # Connect actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        self.exitAction.triggered.connect(self.close)
        self.copyAddressAction.triggered.connect(lambda event: self.copyName())
        self.variablesAction.triggered.connect(self.variables_settings_of_quest)
        self.helpAction.triggered.connect(self.help_dialog)
        self.runAction.triggered.connect(self.run)

    def copyName(self):
        try:
            pyperclip.copy(self.tree.itemAt(self.clicked_pos).text(0))
        except AttributeError:
            pass

    def run(self):
        if self.current_file != "":
            self.saveFile()
            self.interToolBox = QToolBar("interpretator")
            self.ex = InterPretate(filename=self.current_file)
            self.interToolBox.addWidget(self.ex)
            self.addToolBar(QtCore.Qt.BottomToolBarArea, self.interToolBox)

    def help_dialog(self):  # help dialog
        ui = Help_Dialog()
        ui.show()
        ui.exec_()

    def variables_settings_of_quest(self):  # variables settings
        if DEBUG:
            print(self.variables)
        VariablesSettings(self.variables, parent=self).show()
        if DEBUG:
            print(self.variables)

    def fill_item(self, item, value: dict):
        item.setExpanded(True)  # on expanded mode of widget it's work
        for key, val in sorted(value.items()):  # cycle on dict
            child = IdQTreeWidgetItem(key)  # create new widget of child
            child.setText(
                0, self.description_data[int(key)]["name"]
            )  # set text of child
            item.addChild(child)  # add child to item
            self.fill_item(child, val)  # filling child

    def fill_widget(
        self, widget, value
    ):  # create visualization of quest's graph by filling widget with value
        widget.clear()  # clearing data
        self.fill_item(
            widget.invisibleRootItem(), value
        )  # start recursive filling of tree

    def change_vertex(self, item):  # change vertex
        # get all way to current vertex in guide
        normal_way = self.get_id_way_by_item(item)[::-1]
        # if this item already opened we mustn't open it again, just set it current
        if self.description_data[normal_way[-1]]["name"] in self.opened_tabs:
            self.settings_storage.setCurrentIndex(
                [
                    index
                    for index in range(self.settings_storage.count())
                    if self.settings_storage.widget(index).name
                    == self.description_data[normal_way[-1]]["name"]
                ][0]
            )
        else:
            if DEBUG:
                print(self.variables)
            self.current_item_settings = TimeforkSettings(
                normal_way,
                self.description_data,
                self.variables,
                self.counter,
                main_widget=self,
            )  # init vertex settings
            self.current_item_settings.setGeometry(QtCore.QRect(311, 311, 721, 721))
            index = self.settings_storage.addTab(
                self.current_item_settings,
                self.description_data[normal_way[-1]]["name"],
            )  # get index of new tab
            self.current_way = normal_way  # change current way to normal
            self.opened_tabs.append(
                self.description_data[normal_way[-1]]["name"]
            )  # add new tab to list of opened tabs

            self.settings_storage.setCurrentIndex(index)

    def change_current_widget(
        self, index
    ):  # changing all variables to change current tab
        if DEBUG:
            print(index)
        self.current_item_settings = self.settings_storage.widget(index)
        self.current_way = self.current_item_settings.normal_way

    def treeMenu(self, pos):
        menu = QMenu()
        menu.addAction(self.copyAddressAction)
        self.clicked_pos = pos
        menu.exec_(QtGui.QCursor.pos())

    def close_tab(self, index):
        self.current_index = self.settings_storage.currentIndex()
        self.change_current_widget(index)
        self.save_current_settings_item()
        self.change_current_widget(self.current_index)
        self.settings_storage.setCurrentIndex(self.current_index)
        self.opened_tabs.remove(self.settings_storage.widget(index).name)
        self.settings_storage.removeTab(index)

    def get_id_way_by_item(self, item):
        arr_of_names = [item.data()]
        now = item
        while True:
            parent = now.parent()
            if parent.data() is None:
                break
            now = parent
            arr_of_names.append(parent.data())
        if DEBUG:
            print(arr_of_names)
        end = []
        for name in arr_of_names:
            for j in range(len(self.description_data)):
                if self.description_data[j]["name"] == name:
                    end.append(j)
        if DEBUG:
            print(end)
        return end

    def save_current_settings_item(self):
        if DEBUG:
            print(self.current_item_settings.name, self.guide_data)
        errors_arr = self.current_item_settings.validate()
        if errors_arr:
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("\n".join(errors_arr))
            msgBox.setWindowTitle("This way is elder")
            msgBox.setStandardButtons(QMessageBox.Ok)

            msgBox.exec_()
            if DEBUG:
                print("No valid")
            return 0
        try:
            id_list = self.current_item_settings.allinConsole()
        except AttributeError:
            return 0
        try:
            if DEBUG:
                print(self.current_way)
            try:
                dic = getFromDict(self.guide_data, [str(i) for i in self.current_way])
            except KeyError:
                return 0
        except AttributeError:
            return 0
        name_list = [self.description_data[i]["name"] for i in map(int, dic.keys())]
        idid = [i for i in map(int, dic.keys())]
        new_name_list = []
        if DEBUG:
            print(dic, self.current_way)
        if DEBUG:
            print(id_list, name_list, idid, self.description_data, self.current_way)
        for item in id_list["components"]:
            if item["type"] == "choice":
                for key, value in item["data"].items():
                    new_name_list.append(value)
                    if not (value in name_list):

                        self.description_data.append({"name": value, "components": []})

                        dic[str(self.counter)] = {}
                        self.counter += 1
                    else:
                        name_list.remove(value)
                if DEBUG:
                    print(dic)
        if DEBUG:
            print(self.description_data, self.guide_data)
        if DEBUG:
            print(new_name_list, idid)
        for item in idid:
            if not (self.description_data[item]["name"] in new_name_list):
                del dic[str(item)]
                self.description_data[item] = {}
            else:
                new_name_list.remove(self.description_data[item]["name"])

        self.fill_widget(self.tree, self.guide_data)

    def saveFile(self):
        if not (self.current_item_settings is None):
            self.save_current_settings_item()
        data = {
            "author": self.authotField.text(),
            "counter": self.counter,
            "variables": self.variables,
            "guide": self.guide_data,
            "description": self.description_data,
        }
        try:
            with open(self.current_file, mode="w", encoding="utf-8") as json_file:
                json.dump(data, json_file)
            db = LastChange(DB_PATH)
            obj = db.filter()
            if obj is not None:
                obj.update(file_path=self.current_file)
            else:
                db.insert(file_path=self.current_file)
        except FileNotFoundError:
            pass

    def close(self):
        sys.exit()

    def newFile(self):
        name = os.path.abspath(
            QFileDialog.getSaveFileName(self, "Save File", filter="json")[0].replace(
                ".json", ""
            )
            + ".json"
        )
        if name == ".json":
            return
        file = open(name, "w")
        text = {
            "author": None,
            "counter": 1,
            "variables": [],
            "guide": {"0": {}},
            "description": [{"name": "Начало", "components": []}],
        }
        json.dump(text, file)
        file.close()
        self.current_file = name
        self.change_data()

    def openFile(self):  # set current file
        self.current_file = os.path.abspath(QFileDialog.getOpenFileName()[0])
        self.change_data()

    def change_data(self):
        (
            author,
            self.counter,
            self.variables,
            self.guide_data,
            self.description_data,
        ) = self.load_json()

        self.authotField.setText(author)  # set self.authorField text to gotten author

        try:  # delecting old Timefork_Setting widget
            self.settings_storage.itemAt(0).widget().setParent(
                None
            )  # set None parent to old Timefork_Setting widget
        except AttributeError:  # ingoring AttributeError if no old Timefork_Setting
            pass

        # create visualization of quest's graph by filling self.tree with gotten data
        self.fill_widget(self.tree, self.guide_data)

    def load_json(
        self,
    ):
        try:
            with open(
                self.current_file, mode="r", encoding="utf-8"
            ) as json_file:  # open current file
                data = json.load(json_file)  # loading data from json using json module
                # return author, counter, guide and description
                return (
                    data["author"],
                    data["counter"],
                    data["variables"],
                    data["guide"],
                    data["description"],
                )
        except FileNotFoundError:
            return "", 0, {}, {}, {}  # return empty data if file not exits


def getFromDict(dataDict, mapList):
    return reduce(operator.getitem, mapList, dataDict)


def setInDict(dataDict, mapList, value):
    getFromDict(dataDict, mapList[:-1])[mapList[-1]] = value


if __name__ == "__main__":
    if "debug" in sys.argv:
        DEBUG = True
    else:
        DEBUG = False

    sys._excepthook = sys.excepthook

    def exception_hook(exctype, value, tb):
        import traceback

        with open(os.path.join(ROOT, "d.log"), "w", encoding="utf-8") as f:
            f.write("".join(traceback.format_exception(exctype, value, tb)))
        print(exctype, value, traceback)
        sys._excepthook(exctype, value, traceback)
        # sys.exit(1)

    sys.excepthook = exception_hook

    app = QApplication(sys.argv)
    ex = TimeFork()
    ex.show()
    sys.exit(app.exec_())
