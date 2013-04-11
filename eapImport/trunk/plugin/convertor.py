#coding=utf-8
from element import Element
from vyhladavac import Vyhladavac
from dictionary import Dictionary
import os


class Convertor:
    (SINGLE) = (0)

    LOAD_TABLE = (
        (SINGLE, "t_package", "name", "Parent_ID=0", "root", "name"),
        (2)
    )

    def __init__(self, paAdapter, paFile):
        self.adapter = paAdapter
        self.aSourceFile = paFile
        self.aVyhladavac = Vyhladavac ()
        self.aVyhladavac.connect_db (paFile)
        self.read ()
        if paAdapter is not None:
            self.write ()


    def _choose(self, paList, paName):
        for x in paList:
            if x.name == paName:
                return x

    def load(self):
        self._choose (self.adapter.templates,
                      "Empty UML diagram").create_new_project ()
        self._load_line ()
        for a in self.LOAD_TABLE:
            if (self.LOAD_TABLE[0] == self.SINGLE):
                self._load_line (a)


    def _load_line(self, *paLine):
        if (paLine[0] == self.SINGLE):
            dest = self.paths[paLine[4]]
            dest = self.aVyhladavac.get_one_item (paLine[1], paLine[2],
                                                  paLine[3])

    def read(self):
        result = self.aVyhladavac.get_items ("t_package",
                                             "Package_ID,Parent_ID,Name",
                                             "Parent_ID=0")
        #t_packge=sorted(t_packge[1:],key=lambda a:a[0])
        self.aRoot = Element (result[0][0], result[0][1],
                              pa_type=Dictionary.ELEMENT_TYPE["Package"],
                              pa_name=result[0][2])

        self.aRoot.read (self.aVyhladavac)

    def write(self):
        self._choose (self.adapter.templates,
                      "Empty UML diagram").create_new_project ()
        self.adapter.project.root.values["name"] = self.aRoot.name
        self.aRoot.write (self.adapter.project.root,
                          self.adapter.project.metamodel)

if __name__ == "__main__":
    c = Convertor (None, os.path.realpath ("d:/temp/model.eap"))
