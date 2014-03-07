#coding=utf-8
__author__ = 'Michal Petrovič'

import re
import logging
import convertor


class Diagram:

    PROPERTIES = (
        ("name", 4),
        ("note", 8, lambda x: re.sub("<(.*?)>", '', x or "")),
    )

    def __init__(self, pa_diagram, pa_parent_package, pa_parent_element, pa_type, pa_name):
        self.name = pa_name
        self.type = pa_type
        self.connections = []
        self.elements = []
        self.values = {}
        self.stored_tables = None
        self.reference = None

        self.diagram_id = pa_diagram
        self.parent_package_id = pa_parent_package
        self.parent_id = pa_parent_element

        self._logger = logging.getLogger(convertor.Convertor.LOGGER_NAME)

    def read(self, pa_table_store):
        self.stored_tables = pa_table_store
        self._read_properties()

    def write(self, pa_reference):
        self.reference = pa_reference
        self._write_properties()

    def _read_properties(self):
        t_diagram = self.stored_tables.get_table('t_diagram')
        filtered_table = filter(lambda x: x[0] == self.diagram_id, t_diagram)[0]

        for a in Diagram.PROPERTIES:
            try:
                if len(a) == 2:
                    value = filtered_table[a[1]]
                elif len(a) == 3 and callable(a[2]):
                    value = a[2](filtered_table[a[1]])
                elif len(a) == 3 and not callable(a[2]):
                    value = a[2][filtered_table[a[1]]]

                self._logger.debug("read diagram property: " + unicode(a[0]) + " = " + unicode(value))
                self.values[a[0]] = value
            except KeyError:
                self._logger.warning("Value " + unicode(value) + " for: " + a[0] + " is not supported!")
                continue

    def _write_properties(self):
        for a in self.values:
            self._logger.debug("write diagram property: " + a + " = " + (unicode(self.values[a]) or ''))
            self.reference.values[a] = (self.values[a] or '')
