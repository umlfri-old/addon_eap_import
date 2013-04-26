#coding=utf-8
__author__='Michal Petrovič'
from comtypesReader import *


class TableStore:

    def __init__(self, filepath):
        self.reader=ComtypesReader()
        self.reader.connect_db(filepath)
        self.loaded_tables={}

    def get_table(self,pa_table_name):
        if not self.loaded_tables.has_key(pa_table_name):
            self.loaded_tables[pa_table_name]=self.reader.get_table(pa_table_name)
        return self.loaded_tables[pa_table_name]
