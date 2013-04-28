#coding=utf-8
__author__='Michal Petrovič'


class Diagram:
    PROPERTIES=(
        ("name",4),
        ("note",8)
    )

    def __init__(self,pa_diagram,pa_parent_package,pa_parent_element,pa_type,pa_name):
        self.name=pa_name
        self.type=pa_type
        self.connections=[]
        self.elements=[]
        self.values={}

        self.diagram_id=pa_diagram
        self.parent_package_id=pa_parent_package
        self.parent_id=pa_parent_element

    def read(self,pa_table_store):
        self.stored_tables=pa_table_store
        self._read_properties()

    def write(self,pa_reference):
        self.reference=pa_reference
        self._write_properties()

    def _read_properties(self):
        t_diagram=self.stored_tables.get_table('t_diagram')
        filtered_table=filter(lambda a:a[0] == self.diagram_id,t_diagram)[0]

        for a in Diagram.PROPERTIES:
            try:
                if len(a) == 2:
                    value=filtered_table[a[1]]
                else:
                    value=a[2][filtered_table[a[1]]]

                print "read diagram property: " + str(a[0]) + " = " + str(value)
                self.values[a[0]]=value
            except KeyError:
                print "Value " + str(value) + " for: " + a[0] + " is not supported!"
                continue

    def _write_properties(self):
        for a in self.values:
            print "write diagram property: "+a+" = "+(str(self.values[a]) or '')
            self.reference.values[a]=(self.values[a] or '')
