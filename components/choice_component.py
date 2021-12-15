from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QLineEdit,
    QSizePolicy,
    QPushButton,
    QHBoxLayout,
    QWidget,
    QGridLayout,
)
from components.component import Component
from widgets_files.arab_button import ArabButton


class ChoiceComponent(Component):
    def _setup(self, description):
        self._setupUI()
        self.description = description
        self.choice_count = 2
        self.choices = []
        self._setupBE(description)

    def _setupUI(self):
        # create dummy widget to set correct position on layout
        # set sizes of self.verticalLayoutWidget
        self.verticalLayoutWidget = QGridLayout(self)
        self.verticalLayoutWidget.setAlignment(
            QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter
        )

        self.addButton = QPushButton(self)
        self.addButton.setText("+")
        self.addButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.addButton.clicked.connect(self.moveButton)

        self.verticalLayoutWidget.addWidget(self.addButton, 0, 0, 2, 0)

    def _setupBE(self, description):
        for key, value in description.get("data", {}).items():
            print(key, value)
            newChoise = QWidget()
            ly = QHBoxLayout()
            le = QLineEdit()
            le.setText(key)
            ly.addWidget(le)

            cb = QLineEdit()
            cb.setText(value)
            cb.setPlaceholderText("Name of new timefork...")
            ly.addWidget(cb)

            newChoise.setLayout(ly)
            arab = ArabButton(self, newChoise)
            self.choice_count += 1
            self.verticalLayoutWidget.addWidget(newChoise, self.choice_count, 0)
            self.verticalLayoutWidget.addWidget(arab, self.choice_count, 1)

            self.choices.append(newChoise)

    def moveButton(self):
        newChoise = QWidget()
        ly = QHBoxLayout()
        le = QLineEdit()
        ly.addWidget(le)

        cb = QLineEdit()
        cb.setPlaceholderText("Name of new timefork...")
        ly.addWidget(cb)

        newChoise.setLayout(ly)
        arab = ArabButton(
            self,
            newChoise,
            function_to_parent_on_close=lambda: self.choices.remove(newChoise),
        )
        self.choice_count += 1
        self.verticalLayoutWidget.addWidget(newChoise, self.choice_count, 0)
        self.verticalLayoutWidget.addWidget(arab, self.choice_count, 1)

        self.choices.append(newChoise)

    def validate(self):
        new_names = [
            widget.layout().itemAt(1).widget().text() for widget in self.choices
        ]
        if len(new_names) == len(set(new_names)):
            arr = []
            name_arr = [i["name"] for i in self.mw.description_data]
            for i in [
                widget.layout().itemAt(1).widget().text() for widget in self.choices
            ]:
                if i in name_arr and not (
                    [
                        self.description.get("data", {})[j]
                        for j in self.description.get("data", {}).keys()
                    ]
                ):
                    arr.append(f'"{i}" already exist')

            return arr
        else:
            return ["New ways have same names"]

    def returnValue(self):
        return {
            "type": "choice",
            "data": {
                widget.layout()
                .itemAt(0)
                .widget()
                .text(): widget.layout()
                .itemAt(1)
                .widget()
                .text()
                for widget in self.choices
            },
        }
