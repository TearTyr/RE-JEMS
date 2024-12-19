import bpy

# Import operator classes from other files in the operators directory
from .action_operators import ReJemsAlterPickActionOperator
from .bone_operators import ReJemsAlterPickBoneOperator, ReJemsAlterAddBoneOperator, ReJemsAlterRemoveBoneOperator
from .core_operators import ReJemsAlterOperator

# List of operator classes for registration
classes = [
    ReJemsAlterOperator,
    ReJemsAlterPickBoneOperator,
    ReJemsAlterAddBoneOperator,
    ReJemsAlterRemoveBoneOperator,
    ReJemsAlterPickActionOperator,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)