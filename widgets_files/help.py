import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog

ROOT = os.path.abspath(__file__)
if ROOT.endswith(".pyc"):
    ROOT = "\\".join(ROOT.split("\\")[:-4])
else:
    ROOT = "\\".join(ROOT.split("\\")[:-2])

print(os.path.join(ROOT, "photos"))


class Help_Dialog(QDialog):
    def __init__(self):
        super(Help_Dialog, self).__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.webEngineView = QtWidgets.QTextEdit(self.centralwidget)
        self.webEngineView.setReadOnly(True)
        html = r"""<!DOCTYPE html>
<html>
    <head>
        <style>
        table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }
        td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        }
        tr:nth-child(even) {
        background-color: #dddddd;
        }
        </style>
    </head>
    <body>
        <h1>Введение</h1>
        <p>Здравствуй, Уважаемый пользователь!</p>
        <p>Спасибо, что вы выбрали наше (моё) приложение!</p>
        <p>TimeFork - движок для создания и интерпретации текстовых квестов. Далее вы можете ознакомиться с руководством пользования данным приложением.</p>
        <h1>Работа с программой</h1>
        <h3>Интерфейс</h3>
        <p>После запуска приложения вас встречает простой интерфейс для пользования программой. Разберем его подробнее:</p>
        <ol>
            <li>
                <p>Меню File со следующими возможностями: создание нового файла, открытие уже созданого, сохранение и выход из программы</p>
                <img src="$\file.png" alt="Файл">
            </li>
            <li>
                <p>Меню Tools со следующими возможностями: Help(руководство пользования) и меню Variables (один из компонентов для создания квестов, см. далее)</p>
                <img src="$\tools.png" alt="Инструменты">
            </li>
            <li>
                <p>Меню хот-клавиш: Новый файл, Открыть уже готовый, Сохранение (действует сочетание Ctrl + S), меню Variables и меню Run для запуска готового квеста</p>
                <img src="$\toolboxes.png" alt="HotBar">
            </li>
            <li>
                <p>Меню веток квестов: при создании нового файла изначально будет только одна ветка: Начало. Для открытия редактирования ветки сделайте двойной клик по названию ветки</p>
                <img src="$\graph.png" alt="граф">
            </li>
            <li>
                <p>
                    При открытии меню редактирования ветки вас встретил поле "Add components...". Всего компонентов 4: text, choise, goto, variables
                </p>
                <img src="$\choicer.png" alt="Выборы">
                <img src="$\components.png" alt="Компоненты">
                <ul>
                    <li>text - компонент, позволяющий добавить описание к ветке, которое увидит пользователь при попадании на неё.</li>
                    <li>choise - компонент, позволяющий добавить выбор к ветке для продвижения по квесту</li>
                    <li>goto - компонент, позволяющий отправиться на одну из веток, т.е. если в данной ветке выбрать компонент goto, то пользователь отправится на указанную ветку</li>
                    <li>variables - компонент, позволяющий добавить различные переменные в квест и совершать с ними различные операции. Переменные добавляются при помощи меню Variаbles, после  этого они будут доступны в компоненте. Данный компонент позволяет добавить hp персонажу, количество денег, какое-либо другое количество и изменять их количество, используя простые математические операции</li>
                </ul>
                <p><b>!ВНИМАНИЕ! ДОБАВЛЯТЬ КОМПОНЕНТЫ ПОСЛЕ ДОБАВЛЕНИЕ goto ИЛИ choise НЕВОЗМОЖНО!</b></p>
            </li>
        </ol>
        <h3>Компоненты</h3>
        <p>Разберем каждый компонент подробнее.</p>
        <ol>
            <li>
                <p>text. При добавлении данного компонента перед пользователем появляется окно, где он может добавить любое описание для ветки, тем самым создать историю для квеста, создать диалоги и т.п.</p>
                <img src="$\text.png" alt="text">
            </li>
            <li>
                <p>choise. При добавлении компонента choise перед пользователем появляется окно, в левой части пользователь вводит имя ветки, которое будет являться id ветки. Именно по этому имени будет происходить переход,
               к примеру, с помощью goto. В правой части вводится имя ветки, которое будет отображаться в редакторе для удобства создателю квеста. Кнопка "+" добавляет новые выборы, "-" убирает их. Большой "-" позволяет убрать компонент</p>
                <img src="$\choice.png">
            </li>
            <li>
                <p>
                    <p>goto. При добавлении компонента gotо появляется окно "goto", которое позволяет задать имя ветки, в которую вернется пользователь, если он выбрал данный вариант ответа. Получить имя ветки для перехода можно дву способами:</p>
                    <img src="$\goto.png">
                </p>
                <ul>
                    <li>взять имя ветки в редакторе в компоненте choise</li>
                    <li>нажать ПКМ во ветке и выбрать "Copy Name*</li>
                </ul>
            </li>
            <li>
                <p>
                    variables. При добавлении данного компонента появляется окно со следующими возможностями: "⭯" для обновления списка переменных в компоненте, выбор созданных переменных, операции для их изменения и число, изменение на которое происходит.
                </p>
                <img src="$\variable.png">
                <p>
                    <b>!В начале квеста необходимо присвоить изначальное значение переменной с помощью "=".!</b>
                </p>

            </li>
        </ol>
        <p>Вариантов использования данных компонентов огромное количество, всё в Вашей фантазии!</p>

        <p>Далее обратимся к кнопке Run на хот-баре. Данная кнопка позволяет запустить интерпретатор по данному квесту. Также можно выбрать уже готовый квест, нажав на кнопку выбора рядом со строкой пути. (перед этим необходимо стереть предыдущий путь)</p>
        <img src="$\interpretate.png">
        <p>Выбирая номер ответа, вы можете продвигаться по квесту, тем самым проходя его или тестируя!</p>

        <p><b>Спасибо за выбор приложения, Приятного пользования!</b></p>
            </body>
        </html>""".replace(
            "$", os.path.join(ROOT, "photos")
        )
        print(html)
        self.webEngineView.setHtml(html)
        self.verticalLayout.addWidget(self.webEngineView)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok
        )
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Help_Dialog()
    ui.show()
    sys.exit(app.exec_())
