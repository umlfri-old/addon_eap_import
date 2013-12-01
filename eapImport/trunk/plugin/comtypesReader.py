#coding=utf-8
__author__ = 'Michal Petrovič'

from comtypes.client import *


class ComtypesReader:

    def __init__(self, file_path):
        com_object = CreateObject("DAO.DBEngine.36")
        self.database = com_object.OpenDatabase(file_path)

    def get_item(self, table_name, column_name, conditions):
        num_rows = self.get_num_rows(table_name, conditions)
        if num_rows != 0:
            rs = self.database.OpenRecordset("SELECT " + column_name + " FROM " + table_name + " WHERE " + conditions)
            return rs.Fields(0).Value
        else:
            return None

    def get_items(self, table_name, columns, conditions):
        num_rows = self.get_num_rows(table_name, conditions)

        rs = self.database.OpenRecordset("SELECT " + columns + " FROM " + table_name + " WHERE " + conditions)
        num_col = rs.Fields.Count
        table = [[None for _ in range(num_col)] for _ in range(num_rows)]

        for a in range(num_rows):
            for b in range(num_col):
                table[a][b] = rs.Fields(b).Value
            rs.MoveNext()

        return table

    def get_num_rows(self, table_name, conditions=None):
        if conditions is None:
            rs = self.database.OpenRecordset("SELECT COUNT(*) FROM " + table_name)
            return rs.Fields(0).Value
        else:
            rs = self.database.OpenRecordset("SELECT COUNT(*) FROM " + table_name + " WHERE " + conditions)
            return rs.Fields(0).Value

    def get_table(self, table_name):
        rs = self.database.OpenRecordset("SELECT * FROM " + table_name)
        x = self.get_num_rows(table_name)
        y = rs.Fields.Count
        table = [[None for _ in range(y)] for _ in range(x)]

        for a in range(x):
            for b in range(y):
                table[a][b] = rs.Fields(b).Value
            rs.MoveNext()

        return table