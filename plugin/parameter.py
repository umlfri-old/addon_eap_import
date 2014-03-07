#coding=utf-8
__author__ = 'Michal Petrovič'

import re
import logging
import convertor


class Parameter:

    PROPERTIES = (
        ("name", 1),
        ("default", 3),
        ("note", 4, lambda x: re.sub("<(.*?)>", '', x or "")),
        ("const", 6,
         {
             False: "False",
             True: "True"
         }
         ),
        ("scope", 8,
         {
             "in": "in",
             "out": "out",
             "inout": "in out"
         }
         ),
        ("type", 2)
    )

    def __init__(self, operation_id, position):
        self.operation_id = operation_id
        self.position = position
        self.values = {}
        self._source_row = None
        self.reference = None
        self.operation_position = None

        self._logger = logging.getLogger(convertor.Convertor.LOGGER_NAME)

    def read(self, table_row):
        self._source_row = table_row
        self._read_properties()

    def write(self, self_reference, operation_position):
        self.reference = self_reference
        self.operation_position = operation_position
        self._write_properties()

    def _read_properties(self):
        for a in Parameter.PROPERTIES:
            try:
                if len(a) == 2:
                    value = self._source_row[a[1]]
                elif len(a) == 3 and callable(a[2]):
                    value = a[2](self._source_row[a[1]])
                elif len(a) == 3 and not callable(a[2]):
                    value = a[2][self._source_row[a[1]]]

                self._logger.debug("read parameter property: " + unicode(a[0]) + " = " + unicode(value))

                self.values[a[0]] = value
            except KeyError:
                self._logger.warning("Value " + unicode(value) + " for: " + a[0] + " is not supported!")
                continue

    def _write_properties(self):
        for a in self.values:
            self._logger.debug("write parameter property: " + a + " = " + (self.values[a] or ''))
            self.reference.values['operations[' + unicode(self.operation_position) + '].parameters[' + unicode(self.position) + '].' + a] = (self.values[a] or '')