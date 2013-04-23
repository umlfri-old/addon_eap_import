#coding=utf-8
from comtypesReader import *


class TableStore:
    TABLES=(
        "t_package",
        "t_diagram",
        "t_object"
    )

    def __init__(self, filepath):
        self.reader=ComtypesReader()
        self.reader.connect_db(filepath)
        self.loaded_tables={}

        self.load_tables()

    def load_tables(self):
        for a in TableStore.TABLES:
            self.loaded_tables[a]=self.reader.get_table(a)


