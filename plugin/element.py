#coding=utf-8
from dictionary import *
class Element:

    def __init__(self,pa_package=None,pa_parent=None,pa_object=None,pa_type=None,pa_name=None):
        self.diagrams=[]
        self.childrens=[]
        self.connections=[]
        self.appears=None

        self.package_ID=pa_package
        self.parent_package_ID=pa_parent
        self.object_ID=pa_object
        self.type=pa_type
        self.name=pa_name


    def read(self,pa_vyhladavac):
        self.vyhladavac=pa_vyhladavac
        self._read_packages()


    def _read_packages(self):
        result=self.vyhladavac.get_items("t_object o",
                                           "Val(o.PDATA1),Package_ID,Object_ID,Object_Type,Name",
                                           "Package_ID=%d and (Not IsNull(o.PDATA1)) and Object_Type='Package'"%self.package_ID)
        if len(result)!=0:
            for a in result:
                new_package=Element(a[0],a[1],a[2],Dictionary.ELEMENT_TYPE[a[3]],a[4])
                print "read "+a[4]
                new_package.read(self.vyhladavac)
                self.childrens.append(new_package)


    def write(self,pa_reference,pa_metamodel):
        self.reference=pa_reference
        self.metamodel=pa_metamodel
        self._write_children()


    def _write_children(self):
        for a in self.childrens:
            print "write "+a.name
            self.reference.create_child_element(self.metamodel.elements[a.type])
            new_child=self._choose(self.reference.children,"Package")
            new_child.values["name"]=a.name
            a.write(new_child,self.metamodel)

    def _choose(self, paList, paName):
        for x in paList:
            if paName in x.name:
                return x