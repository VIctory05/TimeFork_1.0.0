from sqlite3_api import Table


class LastChange(Table):
    file_path: str  # Path to last changed quest


class QuestProgress(Table):
    file_path: str  # Path to last executable quest
    branch: int  # Branch index
