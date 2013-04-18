#coding=utf-8
class Dictionary:

    DIAGRAM_TYPE = {
        "Use Case":"Use Case diagram",
        "Object":"Object diagram",
        "Logical":"Class diagram",
        "Activity":"Activity diagram",
        "Statechart":"State diagram"
    }


    ELEMENT_TYPE = {
        None:"StartState",
        "Package":"Package",
        None:"Decision",
        None:"Object",
        None:"UseCase",
        None:"Actor",
        None:"Class",
        None:"Note",
        None:"Merge",
        None:"State",
        None:"VerticalSynchronization",
        None:"HorizontalSynchronization",
        None:"Activity",
        None:"Interface",
        None:"Boundary",
        None:"EndState"
    }

    CONNECTION_TYPE={
        "Compose",
        "Note Link",
        "Extend",
        "Implementation",
        "Generalization",
        "Dependency",
        "Control Flow",
        "AssociationInstance",
        "StateTransition",
        "Include",
        "AssociationUseCase",
        "Association",
        "Agregation"
    }