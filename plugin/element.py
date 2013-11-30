#coding=utf-8
__author__='Michal Petrovič'
from dictionary import *
from diagram import *
from attribute import *
from operation import *
import re


class Element:

    PROPERTIES=(
        ("name",3),
        ("stereotype",9),
        ("note",7,lambda x:re.sub("<(.*?)>",'',x or "")),
        ("abstract",22,
            {
                '0':"False",
                '1':"True"
            }
        ),
        ("scope",38,
            {
                "Private":"Private",
                "Public":"Public",
                "Protected":"Protected"
            }
        )
    )

    def __init__(self,pa_package,pa_parent,pa_object,pa_type,pa_name):
        self.diagrams=[]
        self.childrens=[]
        self.connections=[]
        self.appears=[]
        self.type=pa_type
        self.name=pa_name

        self.atributes=[]
        self.operations=[]
        self.values={}

        self.package_id=pa_package
        self.parent_package_id=pa_parent
        self.object_id=pa_object


    def read(self,pa_table_store):
        self.stored_tables=pa_table_store

        self._read_properties()
        self._read_appearance_in_diagram()
        self._read_attributes()
        self._read_operations()
        self._read_packages()
        self._read_diagrams()
        self._read_objects()

    def first_write(self,pa_reference,pa_convertor):
        self.convertor=pa_convertor
        self.reference=pa_reference

        self._write_properties()
        self._write_attributes()
        self._write_operations()
        self._write_children()
        self._write_diagrams()

    def second_write(self):
        self._write_appearance_in_diagram()

    def _read_packages(self):
        if self.type == "Package":
            t_object=self.stored_tables.get_table('t_object')
            filtered_table=filter(lambda a:((a[24] != None) and (a[1] == 'Package') and (a[8] == self.package_id)),t_object)

            for a in filtered_table:
                print "read package " + str(a[3])
                new_package=Element(int(a[24]),a[8],a[0],Dictionary.ELEMENT_TYPE[(a[1],int(a[10]))],a[3])
                new_package.read(self.stored_tables)
                self.childrens.append(new_package)

    def _read_diagrams(self):
        t_diagram=self.stored_tables.get_table('t_diagram')

        if self.type == "Package":
            filtered_table=filter(
                lambda a:((a[2] == 0) and (a[1] == self.package_id)),
                t_diagram)
        else:
            filtered_table=filter(
                lambda a:((a[2] == self.object_id)),t_diagram)

        for row in filtered_table:
            print "read diagram " + str(row[4])
            try:
                new_diagram=Diagram(row[0],row[1],row[2],Dictionary.DIAGRAM_TYPE[row[3]],row[4])
            except KeyError:
                continue

            new_diagram.read (self.stored_tables)
            self.diagrams.append(new_diagram)

    def _read_objects(self):
        t_object=self.stored_tables.get_table('t_object')
        if self.type == 'Package':
            filtered_table=filter(
                lambda a:a[1] != 'Package' and a[43] == 0 and a[8] == self.package_id,t_object)
        else:
            filtered_table=filter(
                lambda a:a[1] != 'Package' and a[43] == self.object_id,t_object)

        for a in filtered_table:
            try:
                print 'read object ' + str(a[3])
                new_object=Element(pa_object=a[0],pa_parent=a[43],pa_name=a[3],
                                       pa_type=Dictionary.ELEMENT_TYPE[(a[1],int(a[10]))],pa_package=None)
            except KeyError:
                continue

            new_object.read(self.stored_tables)
            self.childrens.append(new_object)

    def _read_attributes(self):
        if self.type != "Package":
            t_attribute=self.stored_tables.get_table('t_attribute')
            filtered_table=filter(lambda a:a[0] == self.object_id,t_attribute)
            sorted_table=sorted(filtered_table,key=lambda x:x[15])

            for row in sorted_table:
                print "read attribute " + row[1]
                new_attribute=Attribute(row[14],row[0],row[15])
                new_attribute.read(self.stored_tables)
                self.atributes.append(new_attribute)

    def _read_operations(self):
        if self.type != "Package":
            t_operation=self.stored_tables.get_table('t_operation')
            filtered_table=filter(lambda a:a[1] == self.object_id,t_operation)
            sorted_table=sorted(filtered_table,key=lambda x:x[14])

            for row in sorted_table:
                print "read operation " + row[2]
                new_operation=Operation(row[0],row[1],row[14])
                new_operation.read(self.stored_tables)
                self.operations.append(new_operation)

    def _read_properties(self):
        if self.package_id!=1:
            t_object=self.stored_tables.get_table("t_object")
            filtered_table=filter(lambda a:  a[0] == self.object_id, t_object)[0]

            for a in Element.PROPERTIES:
                try:
                    if len(a) == 2:
                        value=filtered_table[a[1]]
                    elif len(a)==3 and callable(a[2]):
                        value=a[2](filtered_table[a[1]])
                    elif len(a)==3 and not callable(a[2]):
                        value=a[2][filtered_table[a[1]]]

                    print "read element property: "+str(a[0])+" = "+str(value)
                    self.values[a[0]]=value
                except KeyError:
                    print "Value "+str(value)+" for: "+a[0]+" is not supported!"
                    continue

    def _read_appearance_in_diagram(self):
        t_diagramobjects=self.stored_tables.get_table("t_diagramobjects")
        filtered_table=filter(lambda a:  a[1] == self.object_id, t_diagramobjects)

        for row in filtered_table:
            self.appears.append(row[0])

    def _write_children(self):
        for a in self.childrens:
            print "write element " + str(a.name)
            new_child=self.reference.create_child_element(self.convertor.get_metamodel().elements[a.type])
            self.convertor.project_elements[a.object_id]=new_child
            a.first_write(new_child,self.convertor)

    def _write_diagrams(self):
        for a in self.diagrams:
            print "write diagram " + str(a.name)
            new_diagram=self.reference.create_diagram(self.convertor.get_metamodel().diagrams[a.type])
            self.convertor.project_diagrams[a.diagram_id]=new_diagram
            a.write(new_diagram)

    def _write_attributes(self):
        for a in self.atributes:
            print "write attribute no. " + str(a.position)
            self.reference.append_item('attributes[' + str(a.position) + ']')
            a.write(self.reference)

    def _write_operations(self):
        for a in self.operations:
            print "write operation no. " + str(a.position)
            self.reference.append_item('operations[' + str(a.position) + ']')
            a.write(self.reference)

    def _write_properties(self):
        for a in self.values:
            try:
                print "write element property: "+a+" = "+(self.values[a] or '')
                self.reference.values[a]=(self.values[a] or '')
            except Exception as e:
                if "Invalid attribute" in e.message:
                    print "Element type: "+self.type+" do not support property "+a
                    continue
                else:
                    raise

    def _write_appearance_in_diagram(self):
        if self.appears:
            for a in self.appears:
                try:
                    print "show element "+(self.name or self.type)+" in diagram "+self.convertor.project_diagrams[a].name
                    self.reference.show_in(self.convertor.project_diagrams[a])
                except KeyError as e:
                    print "Element type "+self.type+" can not display in required diagram"
                    continue

        for a in self.childrens:
                a.second_write()

