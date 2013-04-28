#coding=utf-8
__author__='Michal Petrovič'

from parameter import *

class Operation:

    PROPERTIES=(
        ("name",2),
        ("stereotype",6),
        ("rtype",4),
        ("note",9),
        ("static",7,
            {
                '0':"False",
                '1':"True"
            }
        ),
        ("abstract",11,
            {
                '0':"False",
                '1':"True"
            }
        ),
        ("scope",3,
            {
                "Private":"Private",
                "Public":"Public",
                "Protected":"Protected"
            }
        )
    )

    def __init__(self,pa_operation_id,pa_object_id,pa_position):
        self.object_id=pa_object_id
        self.operation_id=pa_operation_id
        self.position=pa_position
        self.values={}
        self.parameters=[]

    def read(self,pa_table_store):
        self.stored_tables=pa_table_store
        self._read_properties()
        self._read_parameters()

    def write(self,pa_reference):
        self.reference=pa_reference
        self._write_properties()
        self._write_parameters()

    def _read_properties(self):
        t_operation=self.stored_tables.get_table('t_operation')
        filtered_table=filter(lambda a:  a[0] == self.operation_id, t_operation)[0]

        for a in Operation.PROPERTIES:
            try:
                if len(a) == 2:
                    value=filtered_table[a[1]]
                else:
                    value=a[2][filtered_table[a[1]]]

                print "read operation property: "+str(a[0])+" = "+str(value)
                self.values[a[0]]=value
            except KeyError:
                print "Value "+str(value)+" for: "+a[0]+" is not supported!"
                continue

    def _read_parameters(self):
        t_operation_params=self.stored_tables.get_table('t_operationparams')
        filtered_table=filter(lambda a:  a[0] == self.operation_id, t_operation_params)
        sorted_table=sorted(filtered_table,key=lambda x:x[5])

        if len(sorted_table)!=0:
            for row in sorted_table:
                print "read operation parameter: "+row[1]
                new_parameter=Parameter(self.operation_id,row[5])
                new_parameter.read(row)
                self.parameters.append(new_parameter)

    def _write_properties(self):
        for a in self.values:
            print "write operation property: "+a+" = "+(self.values[a] or '')
            self.reference.values['operations['+str(self.position)+'].'+a]=(self.values[a] or '')


    def _write_parameters(self):
        for a in self.parameters:
            print "write operation parameter: "+a.values['name']
            self.reference.append_item('operations['+str(self.position)+'].parameters['+str(a.position)+']')
            a.write(self.reference,self.position)