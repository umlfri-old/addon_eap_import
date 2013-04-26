#coding=utf-8
__author__='Michal Petrovič'
from dictionary import *
from diagram import *
from attribute import *
from operation import *


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

        self.package_id=pa_package
        self.parent_package_id=pa_parent
        self.object_id=pa_object


    def read(self, pa_table_store):
        self.stored_tables=pa_table_store
        self._read_packages()
        self._read_diagrams()
        self._read_objects()
        self._read_attributes()
        self._read_operations()


    def _read_packages(self):
        if self.type == "Package":
            t_object=self.stored_tables.get_table('t_object')
            filtered_table=filter(lambda a: (
                (a[24] != None) and (a[1] == 'Package') and (
                    a[8] == self.package_id)),
                                  t_object)
            if len(filtered_table) != 0:
                for a in filtered_table:
                    print "read package " + str(a[3])
                    new_package=Element(int(a[24]), a[8], a[0],
                                        Dictionary.ELEMENT_TYPE[
                                            (a[1], int(a[10]))], a[3])
                    new_package.read(self.stored_tables)
                    self.childrens.append(new_package)


    def _read_diagrams(self):
        t_diagram=self.stored_tables.get_table('t_diagram')

        if self.type == "Package":
            filtered_table=filter(
                lambda a: ((a[2] == 0) and (a[1] == self.package_id)),
                t_diagram)
        else:
            filtered_table=filter(
                lambda a: ((a[2] == self.object_id)), t_diagram)

        if len(filtered_table) != 0:
            for a in filtered_table:

                print "read diagram " + str(a[4])
                try:
                    new_diagram=Diagram(a[0], a[1], a[2],
                                        Dictionary.DIAGRAM_TYPE[a[3]], a[4])
                    print "read diagram " + str(a[4])
                except KeyError:
                    continue

                #new_diagram.read (self.vyhladavac)
                self.diagrams.append(new_diagram)

    def _read_objects(self):
        t_object=self.stored_tables.get_table('t_object')
        if self.type == 'Package':
            filtered_table=filter(
                lambda a: a[1] != 'Package' and a[43] == 0 and a[
                    8] == self.package_id, t_object)
        else:
            filtered_table=filter(
                lambda a: a[1] != 'Package' and a[43] == self.object_id,
                t_object)

        if len(filtered_table) != 0:
            for a in filtered_table:
                try:
                    print 'read object ' + str(a[3])
                    new_object=Element(pa_object=a[0], pa_parent=a[43],
                                       pa_name=a[3],
                                       pa_type=Dictionary.ELEMENT_TYPE[
                                           (a[1], int(a[10]))])
                except KeyError:
                    continue

                new_object.read(self.stored_tables)
                self.childrens.append(new_object)

    def _read_attributes(self):
        if self.type!= "Package":
            t_attribute=self.stored_tables.get_table('t_attribute')
            filtered_table=filter(lambda a:  a[0] == self.object_id, t_attribute)
            sorted_table=sorted(filtered_table,key=lambda x:x[15])

            if len(sorted_table)!=0:
                for row in sorted_table:
                    print "read attribute "+row[1]
                    new_attribute=Attribute(row[14],row[0],row[15])
                    new_attribute.read(self.stored_tables)
                    self.atributes.append(new_attribute)

    def _read_operations(self):
        if self.type!= "Package":
            t_operation=self.stored_tables.get_table('t_operation')
            filtered_table=filter(lambda a:  a[1] == self.object_id, t_operation)
            sorted_table=sorted(filtered_table,key=lambda x:x[14])

            if len(sorted_table)!=0:
                for row in sorted_table:
                    print "read operation "+row[2]
                    new_operation=Operation(row[0],row[1],row[14])
                    new_operation.read(self.stored_tables)
                    self.operations.append(new_operation)

    def write(self, pa_reference, pa_metamodel):
        self.reference=pa_reference
        self.metamodel=pa_metamodel
        self._write_children()
        self._write_diagrams()
        self._write_attributes()
        self._write_operations()


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
            #a.write(new_diagram, self.metamodel)

    def _write_attributes(self):
        for a in self.atributes:
            print "write attribute no. " + str(a.position)
            self.reference.append_item('attributes['+str(a.position)+']')
            a.write(self.reference)

    def _write_operations(self):
            for a in self.operations:
                print "write operation no. " + str(a.position)
                self.reference.append_item('operations['+str(a.position)+']')
                a.write(self.reference)

    def _choose(self, paList, paName):
        for x in paList:
            if paName in x.name:
                return x