import bpy
from bpy.props import (
    FloatProperty,
    BoolProperty,
    StringProperty,
    CollectionProperty,
)
from bpy.types import PropertyGroup

class BoneWhitelistItem(PropertyGroup):
    name: StringProperty(
        name="Bone Name",
        description="Name of the bone to exclude from simplification"
    )

class ReJemsAlterProperties(PropertyGroup):
    use_outlier_detection: BoolProperty(
        name="Use Outlier Detection",
        description="Enable outlier detection",
        default=True
    )
    outlier_threshold: FloatProperty(
        name="Outlier Threshold",
        description="Threshold for outlier detection",
        default=3.0,
        min=0.0
    )
    tolerance: FloatProperty(
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