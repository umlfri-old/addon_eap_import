#coding=utf-8
__author__='Michal Petrovič'


class Attribute:

    PROPERTIES=(
        ("name",1),
        ("stereotype",3),
        ("default",23),
        ("note",12),
        ("static",5,
         {
             0:"False",
             1:"True"
         }
        ),
        ("scope",2,
         {
             "Private":"Private",
             "Public":"Public",
             "Protected":"Protected"
         }
        ),
        ("type",24)

    )

    def __init__(self,pa_attribute_id,pa_object_id,pa_position):
        self.object_id=pa_object_id
        self.attribute_id=pa_attribute_id
        self.position=pa_position
        self.values={}

    def read(self,pa_table_store):
        self.stored_tables=pa_table_store
        self._read_properties()

    def write(self,pa_reference):
        self.reference=pa_reference
        self._write_properties()

    def _read_properties(self):
        t_attribute=self.stored_tables.get_table("t_attribute")
        filtered_table=filter(lambda a:  a[14] == self.attribute_id, t_attribute)[0]

        for a in Attribute.PROPERTIES:
            try:
                if len(a) == 2:
                    value=filtered_table[a[1]]
                else:
                    value=a[2][filtered_table[a[1]]]
                print "read atribute property: "+str(a[0])+" = "+str(value)
                self.values[a[0]]=value
            except KeyError:
                print "Value "+str(value)+" for: "+a[0]+" is not supported!"
                continue

    def _write_properties(self):
        for a in self.values:
            print "write attribute property:" +a+" = "+(self.values[a] or '')
            self.reference.values['attributes['+str(self.position)+'].'+a]=(self.values[a] or '')