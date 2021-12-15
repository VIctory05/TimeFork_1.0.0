import json
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from database import QuestProgress, DB_PATH


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        font = QtGui.QFont()
        font.setFamily("System")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        Form.setFont(font)

        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.file = QtWidgets.QLineEdit(Form)
        self.file.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.file)
        self.file_chooser = QtWidgets.QPushButton(Form)
        self.file_chooser.setText("")
        self.file_chooser.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.file_chooser)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setReadOnly(True)
        self.textEdit.setStyleSheet("* {background-color: black; color: green}")
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.answer = QtWidgets.QLineEdit(Form)
        self.answer.setObjectName("lineEdit")
        self.answer.setStyleSheet(
            "* {background-color: black; color: green;border:none}"
        )
        self.textEdit.setStyleSheet("* {background-color: black; color: green}")
        self.verticalLayout.addWidget(self.answer)
        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setCentralWidget(self.centralwidget)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textEdit.setHtml(
            _translate(
                "Form",
                '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">\n'
                '<html><head><meta name="qrichtext" content="1" /><style type="text/css">\n'
                "p, li { white-space: pre-wrap; }\n"
                "</style></head><body style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
                '<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:\'System\'; font-size:15pt; font-weight:600;">Россия</span></p></body></html>',
            )
        )


class InterPretate(QtWidgets.QMainWindow, Ui_Form):
    resumeQuest = QtCore.pyqtSignal(int)

    def __init__(self, filename=None):
        super(InterPretate, self).__init__()
        self.setupUi(self)

        self.file_chooser.clicked.connect(self.setFile)
        self.file.textChanged.connect(self.load_json)
        self.description = []
        self.full_text = ""
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.addLetter)
        self.components = []
        self.branch = {}
        self._i = 0
        self._component_i = 0
        self.variables = {}

        self.resumeQuest.connect(lambda i: self.start_quest(self.branch, i))

        if filename is None:
            db = QuestProgress(DB_PATH)
            obj = db.filter()
            if obj is not None:
                if not os.path.isfile(obj.file_path):
                    db.api.execute("DELETE FROM QuestProgress WHERE id=?", obj.id)
                    db.api.commit()
                else:
                    self.file.setText(obj.file_path)
                    self.textEdit.setPlainText("")
                    self.start_quest(self.description[obj.branch])
        else:
            self.file.setText(filename)

    def setFile(self):
        self.file.setText(os.path.abspath(QFileDialog.getOpenFileName()[0]))

    def load_json(self):
        try:
            with open(self.file.text(), mode="r", encoding="utf-8") as json_file:
                data = json.load(json_file)
                self.description = data["description"]
                self.start_quest(self.description[0])
        except FileNotFoundError:
            return

    def check_answer(self):
        answer = self.answer.text().strip()
        if not answer or not answer.isdigit():
            return
        answer = int(answer)

        choice = self.components[self._component_i]["data"]
        if 1 <= answer <= len(choice):
            branch = [
                obj
                for obj in self.description
                if obj.get("name") == list(choice.values())[answer - 1]
            ][0]
            self.branch = branch
            self._component_i = 0
            self.resumeQuest.emit(0)

    def start_quest(self, data, index: int = 0):
        try:
            self.answer.returnPressed.disconnect()
        except TypeError:
            pass

        self.full_text += "\n"
        self.branch = data
        self.components = self.branch["components"]
        for i, component in enumerate(self.components):
            if i < index:
                continue
            if component["type"] == "text":
                self._component_i = i
                self.timer.start(20)
                break
            elif component["type"] == "choice":
                self.full_text += "\n".join(
                    f"{ind + 1}. {ans}"
                    for ind, ans in enumerate(component["data"].keys())
                )
                self.textEdit.setText(self.full_text)
                self.textEdit.verticalScrollBar().setValue(
                    self.textEdit.verticalScrollBar().maximum()
                )
                self._component_i = i
                self.answer.returnPressed.connect(self.check_answer)
                break
            elif component["type"] == "goto":
                branch = [
                    obj for obj in self.description if obj["name"] == component["data"]
                ][0]
                self.branch = branch
                self.resumeQuest.emit(0)
                break
            elif component["type"] == "variables":
                if component["operation"] == "=":
                    self.variables[component["varname"]] = eval(component["integer"])
                if component["operation"] == "+":
                    self.variables[component["varname"]] += eval(component["integer"])
                if component["operation"] == "-":
                    self.variables[component["varname"]] -= eval(component["integer"])
                if component["operation"] == "*":
                    self.variables[component["varname"]] *= eval(component["integer"])
                if component["operation"] == "/":
                    self.variables[component["varname"]] /= eval(component["integer"])
                if component["operation"] == "%":
                    self.variables[component["varname"]] %= eval(component["integer"])

    def addLetter(self):
        try:
            self.full_text += self.components[self._component_i]["data"][self._i]
            self._i += 1
            self.textEdit.setText(self.full_text)
            self.textEdit.verticalScrollBar().setValue(
                self.textEdit.verticalScrollBar().maximum()
            )
        except IndexError:
            self.timer.stop()
            self.textEdit.verticalScrollBar().setValue(
                self.textEdit.verticalScrollBar().maximum()
            )
            self._i = 0

            self.resumeQuest.emit(self._component_i + 1)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if not self.file.text().strip():
            return event.accept()

        db = QuestProgress(DB_PATH)
        obj = db.filter()
        if (
            QMessageBox.question(
                self,
                "Подтвердите",
                "Вы хотите сохранить прогресс?",
            )
            == QMessageBox.Yes
        ):
            if obj is not None:
                obj.update(
                    file_path=self.file.text(),
                    branch=self.description.index(self.branch),
                )
            else:
                db.insert(
                    file_path=self.file.text(),
                    branch=self.description.index(self.branch),
                )
        else:
            if obj is not None:
                db.api.execute("DELETE FROM QuestProgress WHERE id=?", obj.id)
                db.api.commit()
        event.accept()
