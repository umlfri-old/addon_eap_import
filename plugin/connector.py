#coding=utf-8
__author__ = 'Michal Petrovič'

import re
import logging
import convertor


class Connector:

    PROPERTIES = (
        ("name", 1),
        ("stereotype", 46),
        ("note", 3, lambda x: re.sub("<(.*?)>", '', x or "")),
        ("direction", 2,
         {
             "Unspecified": "Unspecified",
             "Source -> Destination": "Source to Destination",
             "Destination -> Source": "Destination to Source",
             "Bi-Directional": "Bidirectional"
         }
         ),
        ("SCardinality", 6),
        ("DCardinality", 9),
        ("SRole", 12),
        ("DRole", 19),
        ("guard", 50),
        ("weight", 51)
    )

    def __init__(self, connector_id, source_id, destination_id, connector_type):
        self.connector_id = connector_id
        self.source_id = source_id
        self.dest_id = destination_id

        self.type = connector_type
        self.values = {}
        self.appears = []
        self.stored_tables = None
        self.reference = None

        self._logger = logging.getLogger(convertor.Convertor.LOGGER_NAME)

    def read(self, table_store):
        self.stored_tables = table_store
        self._read_properties()

    def write(self, self_reference):
        self.reference = self_reference
        self._write_properties()

    def _read_properties(self):
        t_connector = self.stored_tables.get_table("t_connector")
        filtered_table = filter(lambda x: x[0] == self.connector_id, t_connector)[0]

        for a in Connector.PROPERTIES:
            try:
                if len(a) == 2:
                    value = filtered_table[a[1]]
                elif len(a) == 3 and callable(a[2]):
                    value = a[2](filtered_table[a[1]])
                elif len(a) == 3 and not callable(a[2]):
                    value = a[2][filtered_table[a[1]]]

                self._logger.debug("read connector property: " + unicode(a[0]) + " = " + unicode(value))

                self.values[a[0]] = value
            except KeyError:
                self._logger.warning("Value " + unicode(value) + " for: " + a[0] + " is not supported!")
                continue

    def _write_properties(self):
        for a in self.values:
            self._logger.debug("write connector property: " + a + " = " + (unicode(self.values[a]) or ''))
            try:
                self.reference.values[a] = (self.values[a] or '')
            except Exception as e:
                if "Unknown exception 500: '[\'Invalid attribute" in e.message:
                    self._logger.warning("Connector type: " + self.type + " not suppoort attribute " + a)
                    continue