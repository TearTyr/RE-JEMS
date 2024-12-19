import bpy

# Import panel classes from other files in the panels directory
from .main_panel import ReJemsAlterPanel, ReJemsAlterBoneWhitelistPanel

# List of panel classes for registration
classes = [
    ReJemsAlterPanel,
    ReJemsAlterBoneWhitelistPanel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)