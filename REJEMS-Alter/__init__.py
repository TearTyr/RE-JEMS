bl_info = {
    "name": "RE:JEMS-Alter",
    "author": "TearTyr / L / Meri",
    "version": (1, 3, 7),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > JEMS Tools",
    "description": "Simplifies keyframes (Bezier/Linear, accuracy control).",
    "category": "Animation",
}

import bpy

# Import modules from subfolders
# from .operators import register_operators, unregister_operators
from . import operators
# from .panels import register_panels, unregister_panels
from . import panels
# from .properties import register_properties, unregister_properties
from . import properties

# --- Registration ---

def register():
    properties.register()
    operators.register()
    panels.register()

def unregister():
    properties.unregister()
    operators.unregister()
    panels.unregister()

if __name__ == "__main__":
    register()