#coding=utf-8
__author__='Michal Petrovič'


class Connector:
    PROPERTIES=(
        ("name", 1),
        ("stereotype", 46),
        ("note", 3),
        ("direction", 2,
         {
             "Unspecified":"Unspecified",
             "Source -> Destination":"Source to Destination",
             "Destination -> Source":"Destination to Source",
             "Bi-Directional":"Bidirectional"
         }
        ),
        ("SCardinality", 6),
        ("DCardinality", 9),
        ("SRole", 12),
        ("DRole", 19),
        ("guard", 50),
        ("weight", 51)
    )

    def __init__(self, pa_connector_id, pa_source_id, pa_dest_id, pa_type):
        self.connector_id=pa_connector_id
        self.source_id=pa_source_id
        self.dest_id=pa_dest_id

        self.type=pa_type
        self.values={}
        self.appears=[]

    def read(self, pa_table_store):
        self.stored_tables=pa_table_store
        self._read_properties()

    def write(self, pa_reference):
        self.reference=pa_reference
        self._write_properties()

    def _read_properties(self):
        t_connector=self.stored_tables.get_table("t_connector")
        filtered_table=filter(lambda a:a[0] == self.connector_id, t_connector)[0]

        for a in Connector.PROPERTIES:
            try:
                if len(a) == 2:
                    value=filtered_table[a[1]]
                else:
                    value=a[2][filtered_table[a[1]]]
                print "read connector property: " + str(a[0]) + " = " + str(value)
                self.values[a[0]]=value
            except KeyError:
                print "Value " + str(value) + " for: " + a[0] + " is not supported!"
                continue

    def _write_properties(self):
        for a in self.values:
            print "write connector property: " + a + " = " + (str(self.values[a]) or '')
            try:
                self.reference.values[a]=(self.values[a] or '')
            except Exception as e:
                if "Unknown exception 500: '[\'Invalid attribute" in e.message:
                    print "Connector type: " + self.type + " not suppoort attribute " + a
                    continue