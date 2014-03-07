#coding=utf-8
__author__ = 'Michal Petrovič'

import convertor
from dictionary import *
from diagram import *
from attribute import *
from operation import *
import re
import logging


class Element:

    PROPERTIES = (
        ("name", 3),
        ("stereotype", 9),
        ("note", 7, lambda x: re.sub("<(.*?)>", '', x or "")),
        ("abstract", 22,
            {
                '0': "False",
                '1': "True"
            }
         ),
        ("scope", 38,
            {
                "Private": "Private",
                "Public": "Public",
                "Protected": "Protected"
            }
         )
    )

    def __init__(self, package_id, parent_id, object_id, element_type, name):
        self.diagrams = []
        self.childrens = []
        self.connections = []
        self.appears = []
        self.type = element_type
        self.name = name

        self.atributes = []
        self.operations = []
        self.values = {}
        self.stored_tables = None
        self.convertor = None
        self.reference = None

        self.package_id = package_id
        self.parent_package_id = parent_id
        self.object_id = object_id

        self._logger = logging.getLogger(convertor.Convertor.LOGGER_NAME)

    def read(self, table_store):
        self.stored_tables = table_store

        self._read_properties()
        self._read_appearance_in_diagram()
        self._read_attributes()
        self._read_operations()
        self._read_packages()
        self._read_diagrams()
        self._read_objects()

    def first_write(self, reference, convertor):
        self.convertor = convertor
        self.reference = reference

        self._write_properties()
        self._write_attributes()
        self._write_operations()
        self._write_children()
        self._write_diagrams()

    def second_write(self):
        self._write_appearance_in_diagram()

    def _read_packages(self):
        if self.type == "Package":
            t_object = self.stored_tables.get_table('t_object')
            filtered_table = filter(lambda x: ((x[24] is not None) and (x[1] == 'Package') and (x[8] == self.package_id)), t_object)

            for a in filtered_table:
                self._logger.debug("read package " + unicode(a[3]))
                new_package = Element(int(a[24]), a[8], a[0], Dictionary.ELEMENT_TYPE[(a[1], int(a[10]))], a[3])
                new_package.read(self.stored_tables)
                self.childrens.append(new_package)

    def _read_diagrams(self):
        t_diagram = self.stored_tables.get_table('t_diagram')

        if self.type == "Package":
            filtered_table = filter(lambda a: (a[2] == 0) and (a[1] == self.package_id), t_diagram)
        else:
            filtered_table = filter(
                lambda a: ((a[2] == self.object_id)), t_diagram)

        for row in filtered_table:
            self._logger.debug("read diagram " + unicode(row[4]))
            try:
                new_diagram = Diagram(row[0], row[1], row[2], Dictionary.DIAGRAM_TYPE[row[3]], row[4])
            except KeyError:
                continue

            new_diagram.read(self.stored_tables)
            self.diagrams.append(new_diagram)

    def _read_objects(self):
        t_object = self.stored_tables.get_table('t_object')
        if self.type == 'Package':
            filtered_table = filter(lambda x: x[1] != 'Package' and x[43] == 0 and x[8] == self.package_id, t_object)
        else:
            filtered_table = filter(lambda x: x[1] != 'Package' and x[43] == self.object_id, t_object)

        for a in filtered_table:
            try:
                self._logger.debug('read object ' + unicode(a[3]))
                new_object = Element(object_id=a[0],
                                     parent_id=a[43],
                                     name=a[3],
                                     element_type=Dictionary.ELEMENT_TYPE[(a[1], int(a[10]))], package_id=None)
            except KeyError:
                continue

            new_object.read(self.stored_tables)
            self.childrens.append(new_object)

    def _read_attributes(self):
        if self.type != "Package":
            t_attribute = self.stored_tables.get_table('t_attribute')
            filtered_table = filter(lambda a: a[0] == self.object_id, t_attribute)
            sorted_table = sorted(filtered_table, key=lambda x: x[15])

            for row in sorted_table:
                self._logger.debug("read attribute " + row[1])
                new_attribute = Attribute(row[14], row[0], len(self.atributes))
                new_attribute.read(self.stored_tables)
                self.atributes.append(new_attribute)

    def _read_operations(self):
        if self.type != "Package":
            t_operation = self.stored_tables.get_table('t_operation')
            filtered_table = filter(lambda a: a[1] == self.object_id, t_operation)
            sorted_table = sorted(filtered_table, key=lambda x: x[14])

            for row in sorted_table:
                self._logger.debug("read operation " + row[2])
                new_operation = Operation(row[0], row[1], len(self.operations))
                new_operation.read(self.stored_tables)
                self.operations.append(new_operation)

    def _read_properties(self):
        if self.package_id != 1:
            t_object = self.stored_tables.get_table("t_object")
            filtered_table = filter(lambda x: x[0] == self.object_id, t_object)[0]

            for a in Element.PROPERTIES:
                try:
                    if len(a) == 2:
                        value = filtered_table[a[1]]
                    elif len(a) == 3 and callable(a[2]):
                        value = a[2](filtered_table[a[1]])
                    elif len(a) == 3 and not callable(a[2]):
                        value = a[2][filtered_table[a[1]]]

                    self._logger.debug("read element property: " + unicode(a[0]) + " = " + unicode(value))
                    self.values[a[0]] = value
                except KeyError:
                    self._logger.warning("Value " + unicode(value) + " for: " + a[0] + " is not supported!")
                    continue

    def _read_appearance_in_diagram(self):
        t_diagramobjects = self.stored_tables.get_table("t_diagramobjects")
        filtered_table = filter(lambda a: a[1] == self.object_id, t_diagramobjects)

        for row in filtered_table:
            self.appears.append(row[0])

    def _write_children(self):
        for a in self.childrens:
            self._logger.debug("write element " + unicode(a.name))
            new_child = self.reference.create_child_element(self.convertor.get_metamodel().elements[a.type])
            self.convertor.project_elements[a.object_id] = new_child
            a.first_write(new_child, self.convertor)

    def _write_diagrams(self):
        for a in self.diagrams:
            self._logger.debug("write diagram " + unicode(a.name))
            new_diagram = self.reference.create_diagram(self.convertor.get_metamodel().diagrams[a.type])
            self.convertor.project_diagrams[a.diagram_id] = new_diagram
            a.write(new_diagram)

    def _write_attributes(self):
        for a in self.atributes:
            self._logger.debug("write attribute no. " + unicode(a.position))
            self.reference.append_item('attributes[' + unicode(a.position) + ']')
            a.write(self.reference)

    def _write_operations(self):
        for a in self.operations:
            self._logger.debug("write operation no. " + unicode(a.position))
            self.reference.append_item('operations[' + unicode(a.position) + ']')
            a.write(self.reference)

    def _write_properties(self):
        for a in self.values:
            try:
                self._logger.debug("write element property: " + a + " = " + (self.values[a] or ''))
                self.reference.values[a] = (self.values[a] or '')
            except Exception as e:
                if "Invalid attribute" in e.message:
                    self._logger.warning("Element type: " + self.type + " do not support property " + a)
                    continue
                else:
                    raise

    def _write_appearance_in_diagram(self):
        if self.appears:
            for a in self.appears:
                try:
                    self._logger.debug("show element " + (self.name or self.type) + " in diagram " + self.convertor.project_diagrams[a].name)
                    self.reference.show_in(self.convertor.project_diagrams[a])
                except KeyError as _:
                    self._logger.warning("Element type " + self.type + " can not display in required diagram")
                    continue

        for a in self.childrens:
                a.second_write()