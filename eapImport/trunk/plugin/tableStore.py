#coding=utf-8
__author__ = 'Michal Petrovič'

from comtypesReader import *


class TableStore:

    def __init__(self, filepath):
        self.reader = ComtypesReader(filepath)
        self.loaded_tables = {}

    def get_table(self, pa_table_name):
        if pa_table_name not in self.loaded_tables:
            self.loaded_tables[pa_table_name] = self.reader.get_table(pa_table_name)
        return self.loaded_tables[pa_table_name]
