#coding=utf-8
from element import Element
from vyhladavac import Vyhladavac
from dictionary import Dictionary
import os


class Convertor:
    def __init__(self, paAdapter, paFile):
        self.adapter=paAdapter
        self.aSourceFile=paFile
        self.aVyhladavac=Vyhladavac()
        self.aVyhladavac.connect_db(paFile)
        self.read()
        if paAdapter is not None:
            self.write()


    def _choose(self, paList, paName):
        for x in paList:
            if x.name == paName:
                return x


    def read(self):
        result=self.aVyhladavac.get_items("t_package",
                                          "Package_ID,Parent_ID,Name",
                                          "Parent_ID=0")

        self.aRoot=Element(result[0][0], result[0][1],
                           pa_type=Dictionary.ELEMENT_TYPE["Package"],
                           pa_name=result[0][2])

        self.aRoot.read(self.aVyhladavac)

    def write(self):
        self._choose(self.adapter.templates,
                     "Empty UML diagram").create_new_project()
        self.adapter.project.root.values["name"]=self.aRoot.name
        self.aRoot.write(self.adapter.project.root,
                         self.adapter.project.metamodel)


if __name__ == "__main__":
    c=Convertor(None, os.path.realpath("d:/temp/model.eap"))
