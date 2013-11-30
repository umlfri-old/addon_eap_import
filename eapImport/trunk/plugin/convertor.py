#coding=utf-8
__author__='Michal Petrovič'
import os

from element import *
from tableStore import *
from connector import *

class Convertor:

    def __init__(self, paAdapter, paFile):
        self.adapter=paAdapter
        self.aSourceFile=paFile
        self.stored_tables=TableStore(paFile)

        self._project_diagrams={}
        self._project_elements={}
        self._project_connectors=[]

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
                self.root=Element(sorted_table[0][0],
                                   sorted_table[0][2],
                                   pa_object=None,
                                   pa_type=Dictionary.ELEMENT_TYPE[("Package", 0)],
                                   pa_name=sorted_table[0][1])
                break

        self.root.read(self.stored_tables)
        self._read_connectors()

    def _read_connectors(self):
        t_connector=self.stored_tables.get_table("t_connector")

        for row in t_connector:
            try:
                new_connector=Connector(row[0],row[26],row[27],Dictionary.CONNECTION_TYPE[row[4],row[5]])
                new_connector.read(self.stored_tables)
                self._project_connectors.append(new_connector)
            except KeyError:
                print "Connection type: ("+row[4]+", "+(row[5]or "None")+") is not supported!"
                continue

    '''
                for diagram in self._project_elements[row[26]].appears:
                    if diagram in self._project_elements[row[27]].appears:
                        new_connector.appears.append(diagram)
    '''

    def write(self):
        self._choose(self.adapter.templates,"Empty UML diagram").create_new_project()
        self.adapter.project.root.values["name"]=self.root.name

        self.root.first_write(self.adapter.project.root,self)
        self.root.second_write()
        self._write_connectors()

    def _write_connectors(self):
        for connector in self._project_connectors:
            if connector.source_id not in self._project_elements or connector.dest_id not in self._project_elements:
                continue
            source=self._project_elements[connector.source_id]
            dest=self._project_elements[connector.dest_id]

            try:
                new_connector=source.connect_with(dest,self.get_metamodel().connections[connector.type])
            except Exception as e:
                if "Unknown exception" in e.message:
                    print "Connector type"+connector.type+" is not supported for "+source.name+" type of element!"
                    continue
            connector.write(new_connector)

            for diagram in source.appears:
                if diagram in dest.appears:
                    new_connector.show_in(diagram)

    def get_metamodel(self):
        if self.adapter.project:
            return self.adapter.project.metamodel

    def add_diagram(self,pa_diagram_id,pa_diagram):
        self._project_diagrams[pa_diagram_id]=pa_diagram

    def get_project_diagrams(self):
        return self._project_diagrams

    def add_element(self,pa_object_id,pa_element):
        self._project_elements[pa_object_id]=pa_element

    def get_project_elements(self):
        return self._project_elements