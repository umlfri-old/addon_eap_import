#coding=utf-8
from dictionary import *
from diagram import *


class Element:
    def __init__(self, pa_package=None, pa_parent=None, pa_object=None,
                 pa_type=None, pa_name=None):
        self.diagrams=[]
        self.childrens=[]
        self.connections=[]
        self.appears=None
        self.type=pa_type
        self.name=pa_name

        self.atributes=[]
        self.operations=[]
        self.values={}

        self.package_ID=pa_package
        self.parent_package_ID=pa_parent
        self.object_ID=pa_object


    def read(self, pa_table_store):
        self.stored_tables=pa_table_store
        self._read_packages()
        self._read_diagrams()
        self._read_objects()


    def _read_packages(self):
        if self.type == "Package":
            t_object=self.stored_tables.loaded_tables['t_object']
            filtered_table=filter(lambda a: (
                (a[24] != None) and (a[1] == 'Package') and (
                    a[8] == self.package_ID)),
                                  t_object)
            if len(filtered_table) != 0:
                for a in filtered_table:
                    new_package=Element(int(a[24]), a[8], a[0],
                                        Dictionary.ELEMENT_TYPE[
                                            (a[1], int(a[10]))], a[3])
                    print "read package " + str(a[3])
                    new_package.read(self.stored_tables)
                    self.childrens.append(new_package)


    def _read_diagrams(self):
        t_diagram=self.stored_tables.loaded_tables['t_diagram']

        if self.type == "Package":
            filtered_table=filter(
                lambda a: ((a[2] == 0) and (a[1] == self.package_ID)),
                t_diagram)
        else:
            filtered_table=filter(
                lambda a: ((a[2] == self.object_ID)), t_diagram)

        if len(filtered_table) != 0:
            for a in filtered_table:

                try:
                    new_diagram=Diagram(a[0], a[1], a[2],
                                        Dictionary.DIAGRAM_TYPE[a[3]], a[4])
                    print "read diagram " + str(a[4])
                except KeyError:
                    continue

                #new_diagram.read (self.vyhladavac)
                self.diagrams.append(new_diagram)

    def _read_objects(self):
        t_object=self.stored_tables.loaded_tables['t_object']
        if self.type == 'Package':
            filtered_table=filter(
                lambda a: a[1] != 'Package' and a[43] == 0 and a[
                    8] == self.package_ID, t_object)
        else:
            filtered_table=filter(
                lambda a: a[1] != 'Package' and a[43] == self.object_ID,
                t_object)

        if len(filtered_table) != 0:
            for a in filtered_table:
                try:
                    new_object=Element(pa_object=a[0], pa_parent=a[43],
                                       pa_name=a[3],
                                       pa_type=Dictionary.ELEMENT_TYPE[
                                           (a[1], int(a[10]))])
                    print 'read object ' + str(a[3])
                except KeyError:
                    continue

                new_object.read(self.stored_tables)
                self.childrens.append(new_object)


    def write(self, pa_reference, pa_metamodel):
        self.reference=pa_reference
        self.metamodel=pa_metamodel
        self._write_children()
        self._write_diagrams()


    def _write_children(self):
        for a in self.childrens:
            print "write children " + str(a.name)
            new_child=self.reference.create_child_element(
                self.metamodel.elements[a.type])
            new_child.values["name"]=a.name
            a.write(new_child, self.metamodel)

    def _write_diagrams(self):
        for a in self.diagrams:
            print "write diagram " + str(a.name)
            new_diagram=self.reference.create_diagram(
                self.metamodel.diagrams[a.type])
            new_diagram.values['name']=a.name
            #            a.write(new_diagram, self.metamodel)


    def _choose(self, paList, paName):
        for x in paList:
            if paName in x.name:
                return x