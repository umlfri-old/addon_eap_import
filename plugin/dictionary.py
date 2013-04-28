#coding=utf-8
__author__='Michal Petrovič'
class Dictionary:

    DIAGRAM_TYPE={
        "Use Case": "Use Case diagram",
        "Object": "Object diagram",
        "Logical": "Class diagram",
        "Activity": "Activity diagram",
        "Statechart": "State diagram"
    }

    ELEMENT_TYPE={
        ("StateNode", 100): "StartState",
        ("StateNode", 3): "StartState",
        ("StateNode", 101): "EndState",
        ("StateNode", 4): "EndState",
        ("Package", 0): "Package",
        ("Decision", 0): "Decision",
        ("Object", 0): "Object",
        ("UseCase", 0): "UseCase",
        ("Actor", 0): "Actor",
        ("Class", 0): "Class",
        ("Note", 0): "Note",
        ("MergeNode", 0): "Merge",
        ("State", 0): "State",
        ("Synchronization", 1): "VerticalSynchronization",
        ("Synchronization", 0): "HorizontalSynchronization",
        ("Activity", 0): "Activity",
        ("Interface", 0): "Interface",
        ("Boundary", 0): "Boundary",
        ("StateNode", 101): "EndState",
        ("StateMachine",8):"State"
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