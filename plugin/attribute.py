#coding=utf-8
__author__ = 'Michal Petrovič'

import re
import logging
import convertor


class Attribute:

    PROPERTIES = (
        ("name", 1),
        ("stereotype", 3),
        ("default", 23),
        ("note", 12, lambda x: re.sub("<(.*?)>", '', x or "")),
        ("static", 5,
         {
             0: "False",
             1: "True"
         }
         ),
        ("scope", 2,
         {
             "Private": "Private",
             "Public": "Public",
             "Protected": "Protected"
         }
         ),
        ("type", 24)

    )

    def __init__(self, attribute_id, object_id, position):
        self.object_id = object_id
        self.attribute_id = attribute_id
        self.position = position
        self.values = {}

        self.stored_tables = None
        self.reference = None

        self._logger = logging.getLogger(convertor.Convertor.LOGGER_NAME)

    def read(self, table_store):
        self.stored_tables = table_store
        self._read_properties()

    def write(self, reference):
        self.reference = reference
        self._write_properties()

    def _read_properties(self):
        t_attribute = self.stored_tables.get_table("t_attribute")
        filtered_table = filter(lambda x: x[14] == self.attribute_id, t_attribute)[0]

        for a in Attribute.PROPERTIES:
            try:
                if len(a) == 2:
                    value = filtered_table[a[1]]
                elif len(a) == 3 and callable(a[2]):
                    value = a[2](filtered_table[a[1]])
                elif len(a) == 3 and not callable(a[2]):
                    value = a[2][filtered_table[a[1]]]

                self._logger.debug("read atribute property: " + unicode(a[0]) + " = " + unicode(value))
                self.values[a[0]] = value
            except KeyError:
                self._logger.warning("Value " + unicode(value) + " for: " + a[0] + " is not supported!")
                continue

    def _write_properties(self):
        for a in self.values:
            self._logger.debug("write attribute property:" + a + " = " + (self.values[a] or ''))
            self.reference.values['attributes[' + unicode(self.position) + '].' + a] = (self.values[a] or '')