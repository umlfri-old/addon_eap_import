#coding=utf-8
__author__ = 'Michal Petrovič'

from element import *
from tableStore import *
from connector import *
import logging
import sys


class Convertor:

    LOGGER_NAME = "eapImport"

    def __init__(self, adapter, file_path):
        self.adapter = adapter
        self.stored_tables = TableStore(file_path)

        self.project_diagrams = {}
        self.project_elements = {}
        self.project_connectors = []
        self.root = None

        self._logger = None

        self._logger_init()

        self._logger.info("START IMPORTING")

        self.read()
        if adapter is not None:
            self.write()

        self._logger.info("IMPORTING FINISHED")

    def _choose(self, sequence, name):
        for x in sequence:
            if x.name == name:
                return x

    def _logger_init(self):
        formater = logging.Formatter('%(levelname)s: %(message)s')
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(formater)
        self._logger = logging.getLogger(Convertor.LOGGER_NAME)
        self._logger.setLevel(level=logging.ERROR)
        self._logger.addHandler(handler)

    def read(self):
        self._logger.info("START READING")
        t_package = self.stored_tables.get_table('t_package')
        sorted_table = sorted(t_package, key=lambda x: x[2])

        for a in sorted_table:
            if a[2] == 0:
                self.root = Element(sorted_table[0][0],
                                    sorted_table[0][2],
                                    object_id=None,
                                    element_type=Dictionary.ELEMENT_TYPE[("Package", 0)],
                                    name=sorted_table[0][1])
                break

        self.root.read(self.stored_tables)
        self._read_connectors()
        self._logger.info("END READING")

    def _read_connectors(self):
        t_connector = self.stored_tables.get_table("t_connector")

        for row in t_connector:
            try:
                new_connector = Connector(row[0], row[26], row[27], Dictionary.CONNECTION_TYPE[row[4], row[5]])
                new_connector.read(self.stored_tables)
                self.project_connectors.append(new_connector)
            except KeyError:
                self._logger.warning("Connection type: (" + row[4] + ", " + (row[5]or "None") + ") is not supported!")
                continue

    '''
                for diagram in self.project_elements[row[26]].appears:
                    if diagram in self.project_elements[row[27]].appears:
                        new_connector.appears.append(diagram)
    '''

    def write(self):
        self._logger.info("START WRITE")
        self._choose(self.adapter.templates, "Empty UML diagram").create_new_project()
        self.adapter.project.root.values["name"] = self.root.name

        self.root.first_write(self.adapter.project.root, self)
        self.root.second_write()
        self._write_connectors()
        self._logger.info("END WRITE")

    def _write_connectors(self):
        for connector in self.project_connectors:
            if connector.source_id not in self.project_elements or connector.dest_id not in self.project_elements:
                continue
            source = self.project_elements[connector.source_id]
            dest = self.project_elements[connector.dest_id]

            try:
                new_connector = source.connect_with(dest, self.get_metamodel().connections[connector.type])
            except Exception as e:
                if "Unknown exception" in e.message:
                    self._logger.warning("Connector type" + connector.type + " is not supported for " +
                                         source.name + '(' + source.type.name + ')' +
                                         " or " + dest.name + '(' + dest.type.name + ") type of element!")
                    continue
            connector.write(new_connector)

            for diagram in source.appears:
                if diagram in dest.appears:
                    new_connector.show_in(diagram)

    def get_metamodel(self):
        if self.adapter.project:
            return self.adapter.project.metamodel