import bpy
from bpy.props import (
    PointerProperty,
)
from bpy.types import Operator, Panel, PropertyGroup

from .operators.core_operator import ReJemsAlterOperator
from .operators.bone_operators import (
    ReJemsAlterPickBoneOperator,
    ReJemsAlterAddBoneOperator,
    ReJemsAlterRemoveBoneOperator,
)
from .panels.main_panel import ReJemsAlterPanel, ReJemsAlterBoneWhitelistPanel
from .properties import ReJemsAlterProperties, BoneWhitelistItem

bl_info = {
    "name": "RE:JEMS-Alter",
    "author": "TearTyr / L / Meri",
    "version": (1, 2, 8),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > JEMS Tools",
    "description": "Simplifies keyframes (Bezier/Linear, accuracy control).",
    "category": "Animation",
}

classes = (
    ReJemsAlterOperator,
    ReJemsAlterPanel,
    ReJemsAlterBoneWhitelistPanel,
    ReJemsAlterPickBoneOperator,
    ReJemsAlterAddBoneOperator,
    ReJemsAlterRemoveBoneOperator,
    ReJemsAlterProperties,
    BoneWhitelistItem,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.rejems_alter_props = PointerProperty(type=ReJemsAlterProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.rejems_alter_props

if __name__ == "__main__":
    register()