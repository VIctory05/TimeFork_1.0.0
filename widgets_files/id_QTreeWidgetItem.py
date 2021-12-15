from PyQt5.QtWidgets import QTreeWidgetItem


class IdQTreeWidgetItem(
    QTreeWidgetItem
):  # creating custom IdQTreeWidgetItem to save id in widget
    def __init__(self, id_):  # special method __init__ run when we initialize widget
        self.id = id_  # save id in widget
        super(IdQTreeWidgetItem, self).__init__()  # initialize QTreeWidgetItem
