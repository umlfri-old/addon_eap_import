#coding=utf-8
class Dictionary:

    DIAGRAM_TYPE = {
        "Use Case diagram",
        "Object diagram",
        "Class diagram",
        "Activity diagram",
        "State diagram"
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