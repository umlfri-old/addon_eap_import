#coding=utf-8
__author__ = 'Michal Petrovič'

from parameter import *
import re
import logging
import convertor


class Operation:

    PROPERTIES = (
        ("name", 2),
        ("stereotype", 6),
        ("rtype", 4),
        ("note", 9, lambda x: re.sub("<(.*?)>", '', x or "")),
        ("static", 7,
            {
                '0': "False",
                '1': "True"
            }
         ),
        ("abstract", 11,
            {
                '0': "False",
                '1': "True"
            }
         ),
        ("scope", 3,
            {
                "Private": "Private",
                "Public": "Public",
                "Protected": "Protected"
            }
         )
    )

    def __init__(self, operation_id, object_id, position):
        self.object_id = object_id
        self.operation_id = operation_id
        self.position = position
        self.values = {}
        self.parameters = []
        self.stored_tables = None
        self.reference = None

        self._logger = logging.getLogger(convertor.Convertor.LOGGER_NAME)

    def read(self, table_store):
        self.stored_tables = table_store
        self._read_properties()
        self._read_parameters()

    def write(self, reference):
        self.reference = reference
        self._write_properties()
        self._write_parameters()

    def _read_properties(self):
        t_operation = self.stored_tables.get_table('t_operation')
        filtered_table = filter(lambda x: x[0] == self.operation_id, t_operation)[0]

        for a in Operation.PROPERTIES:
            try:
                if len(a) == 2:
                    value = filtered_table[a[1]]
                elif len(a) == 3 and callable(a[2]):
                    value = a[2](filtered_table[a[1]])
                elif len(a) == 3 and not callable(a[2]):
                    value = a[2][filtered_table[a[1]]]

                self._logger.debug("read operation property: " + unicode(a[0]) + " = " + unicode(value))
                self.values[a[0]] = value
            except KeyError:
                self._logger.warning("Value " + unicode(value) + "  for: " + a[0] + " is not supported!")
                continue

    def _read_parameters(self):
        t_operation_params = self.stored_tables.get_table('t_operationparams')
        filtered_table = filter(lambda a: a[0] == self.operation_id, t_operation_params)
        sorted_table = sorted(filtered_table, key=lambda x: x[5])

        if len(sorted_table) != 0:
            for row in sorted_table:
                self._logger.debug("read operation parameter: " + row[1])
                new_parameter = Parameter(self.operation_id, row[5])
                new_parameter.read(row)
                self.parameters.append(new_parameter)

    def _write_properties(self):
        for a in self.values:
            self._logger.debug("write operation property: " + a + " = " + (self.values[a] or ''))
            self.reference.values['operations[' + unicode(self.position) + '].' + a] = (self.values[a] or '')

    def _write_parameters(self):
        for a in self.parameters:
            self._logger.debug("write operation parameter: " + a.values['name'])
            self.reference.append_item('operations[' + unicode(self.position) + '].parameters[' + unicode(a.position) + ']')
            a.write(self.reference,self.position)