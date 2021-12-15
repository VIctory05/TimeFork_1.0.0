from .tables import LastChange, QuestProgress

DB_PATH = "database.sqlite"

LastChange(DB_PATH).create_table()
QuestProgress(DB_PATH).create_table()
