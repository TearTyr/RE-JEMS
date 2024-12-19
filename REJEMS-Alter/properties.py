import bpy
from bpy.props import (
    FloatProperty,
    BoolProperty,
    EnumProperty,
    PointerProperty,
    StringProperty,
    IntProperty,
    CollectionProperty,
)
from bpy.types import PropertyGroup

# --- Bone Whitelist Item ---
class BoneWhitelistItem(PropertyGroup):
    name: StringProperty(
        name="Bone Name",
        description="Name of the bone to exclude from simplification"
    )

# --- Property Group ---
class ReJemsAlterProperties(PropertyGroup):
    use_outlier_detection: BoolProperty(
        name="Use Outlier Detection",
        description="Enable outlier detection",
        default=True
    )
    outlier_threshold: FloatProperty(
        name="Threshold for outlier detection",
        description="Threshold for outlier detection",
        default=3.0,
        min=0.0,
        max=10.0
    )
    vw_tolerance: FloatProperty(
        name="VW Tolerance",
        description="Simplification tolerance for Visvalingam-Whyatt",
        default=0.05,
        min=0.0,
        max=1.0
    )
    error_threshold: FloatProperty(
        name="Error Threshold",
        description="Error threshold for JEMS convergence",
        default=0.05,
        min=0.0,
        max=1.0
    )
    max_iterations: IntProperty(
        name="Max Iterations",
        description="Maximum iterations for JEMS algorithm",
        default=100,
        min=1
    )
    initial_learning_rate: FloatProperty(
        name="Initial Learning Rate",
        description="Initial learning rate for JEMS algorithm",
        default=0.2,
        min=0.0,
        max=1.0
    )
    action_name: StringProperty(
        name="Action",
        description="Select the action to simplify"
    )
    selected_bone_name: StringProperty(
        name="Selected Bone",
        description="Selected bone for the whitelist"
    )
    bone_whitelist: CollectionProperty(
        type=BoneWhitelistItem
    )
    advanced_mode: BoolProperty(
        name="Advanced Mode",
        description="Show advanced settings",
        default=False
    )
    show_advanced_settings: BoolProperty(
        name="Show Advanced Settings",
        description="Show advanced settings for simplification",
        default=False
    )
    simplification_mode: EnumProperty(
        name="Simplification Mode",
        description="Choose the simplification mode",
        items=[
            ('BALANCED', "Balanced", "Balances between simplification and accuracy"),
            ('ACCURATE', "Accurate", "Prioritizes accuracy over simplification"),
            ('CUSTOM', "Custom", "Allows custom settings for both VW Tolerance and Error Threshold")
        ],
        default='BALANCED'
    )

def register():
    bpy.utils.register_class(BoneWhitelistItem)
    bpy.utils.register_class(ReJemsAlterProperties)
    bpy.types.Scene.rejems_alter_props = PointerProperty(type=ReJemsAlterProperties)

def unregister():
    del bpy.types.Scene.rejems_alter_props
    bpy.utils.unregister_class(ReJemsAlterProperties)
    bpy.utils.unregister_class(BoneWhitelistItem)