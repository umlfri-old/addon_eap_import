#coding=utf-8
from comtypes.client import *


class ComtypesReader:
    def __init__(self):
        self.aCOM_object=CreateObject("DAO.DBEngine.36")


    def connect_db(self, paPath):
        """
        Pripojí sa k zadanému súboru
        """
        self.aDB=self.aCOM_object.OpenDatabase(paPath)

    def get_one_item(self, paTable, paColumn, paCondition):
        num_rows=self.get_num_rows(paTable, paCondition)
        if (num_rows != 0):
            rs=self.aDB.OpenRecordset(
                "SELECT " + paColumn + " FROM " + paTable + " WHERE " + paCondition)
            return rs.Fields(0).Value
        else:
            return None

    def get_items(self, paTable, paColumn, paCondition):
        num_rows=self.get_num_rows(paTable, paCondition)

        rs=self.aDB.OpenRecordset(
            "SELECT " + paColumn + " FROM " + paTable + " WHERE " + paCondition)
        num_col=rs.Fields.Count
        table=[[None for e in range(num_col)] for f in range(num_rows)]

        for a in range(num_rows):
            for b in range(num_col):
                table[a][b]=rs.Fields(b).Value
            rs.MoveNext()

        return table


    def get_num_rows(self, paTable, paConditions=None):
        if paConditions == None:
            rs=self.aDB.OpenRecordset("SELECT COUNT(*) FROM " + paTable)
            return rs.Fields(0).Value
        else:
            rs=self.aDB.OpenRecordset(
                "SELECT COUNT(*) FROM " + paTable + " WHERE " + paConditions)
            return rs.Fields(0).Value

    def get_table(self, paTable):
        rs=self.aDB.OpenRecordset("SELECT * FROM " + paTable)
        x=self.get_num_rows(paTable)
        y=rs.Fields.Count
        table=[[None for e in range(y)] for f in range(x)]

        for a in range(x):
            for b in range(y):
                table[a][b]=rs.Fields(b).Value
            rs.MoveNext()

        return table

    def choose(self, paList, paName):
        for x in paList:
            if x.name == paName:
                return x



