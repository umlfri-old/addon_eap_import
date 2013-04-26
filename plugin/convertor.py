#coding=utf-8
__author__='Michal Petrovič'
import os

from element import *
from tableStore import *


class Convertor:
    def __init__(self, paAdapter, paFile):
        self.adapter=paAdapter
        self.aSourceFile=paFile
        self.stored_tables=TableStore(paFile)
        self.read()
        if paAdapter is not None:
            self.write()


    def _choose(self, paList, paName):
        for x in paList:
            if x.name == paName:
                return x


    def read(self):
        t_package=self.stored_tables.get_table('t_package')
        sorted_table=sorted(t_package, key=lambda a: a[2])

        for a in sorted_table:
            if a[2] == 0:
                self.aRoot=Element(sorted_table[0][0], sorted_table[0][2],
                                   pa_type=Dictionary.ELEMENT_TYPE[
                                       ("Package", 0)],
                                   pa_name=sorted_table[0][1])
                break

        self.aRoot.read(self.stored_tables)

    def write(self):
        self._choose(self.adapter.templates,
                     "Empty UML diagram").create_new_project()
        self.adapter.project.root.values["name"]=self.aRoot.name
        self.aRoot.write(self.adapter.project.root,
                         self.adapter.project.metamodel)


if __name__ == "__main__":
    c=Convertor(None, os.path.realpath("d:/temp/model.eap"))
