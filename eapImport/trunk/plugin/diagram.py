#coding=utf-8
__author__='Michal Petrovič'
class Diagram:
    def __init__(self, pa_diagram=None, pa_parent_package=None,
                 pa_parent_element=None, pa_type=None, pa_name=None):
        self.name=pa_name
        self.type=pa_type
        self.connections=[]
        self.elements=[]

        self.diagram_ID=pa_diagram
        self.parent_package_ID=pa_parent_package
        self.parent_ID=pa_parent_element
