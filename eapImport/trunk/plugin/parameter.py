#coding=utf-8
__author__='Michal Petrovič'

class Parameter:

    PROPERTIES=(
        ("name",1),
        ("default",3),
        ("note",4),
        ("const",6,
         {
             False:"False",
             True:"True"
         }
        ),
        ("scope",8,
         {
             "in":"in",
             "out":"out",
             "inout":"in out"
         }
        ),
        ("type",2)

    )

    def __init__(self,pa_operation_id,pa_position):
        self.operation_id=pa_operation_id
        self.position=pa_position
        self.loaded_properties={}

    def read(self,pa_table_row):
        self.source_row=pa_table_row
        self._read_properties()

    def write(self,pa_reference,pa_operation_position):
        self.reference=pa_reference
        self.operation_position=pa_operation_position
        self._write_properties()

    def _read_properties(self):
        for a in Parameter.PROPERTIES:
            try:
                if len(a) == 2:
                    value=self.source_row[a[1]]
                else:
                    value=a[2][self.source_row[a[1]]]

                print "read parameter property: "+str(a)+" = "+str(value)
                self.loaded_properties[a[0]]=value
            except KeyError:
                print "Value "+str(value)+" for: "+a[0]+" is not supported!"
                continue

    def _write_properties(self):
        for a in self.loaded_properties:
            print "write parameter property: "+a+" = "+(self.loaded_properties[a] or '')
            self.reference.values['operations['+str(self.operation_position)+'].parameters['+str(self.position)+'].'+a]=(self.loaded_properties[a] or '')