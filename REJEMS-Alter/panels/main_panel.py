import bpy
from bpy.types import Panel

# --- UI Panel ---
class ReJemsAlterPanel(Panel):
    bl_label = "RE:JEMS-Alter"
    bl_idname = "VIEW3D_PT_rejems_alter"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JEMS Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.rejems_alter_props
        obj = context.active_object

        # Action selection with eyedropper
        row = layout.row(align=True)
        row.prop_search(props, "action_name", bpy.data, "actions", text="Select Action")
        row.operator("object.rejems_alter_pick_action", icon='EYEDROPPER', text="")

        layout.operator("object.rejems_alter")

        # Advanced Mode
        layout.prop(props, "advanced_mode")

        if props.advanced_mode:
            # Simplification Settings
            box = layout.box()
            box.label(text="Simplification Settings:")
            row = box.row()
            row.prop(props, "simplification_mode", expand=True)

            if props.simplification_mode == 'BALANCED':
                box.prop(props, "vw_tolerance", slider=True)
            elif props.simplification_mode == 'ACCURATE':
                box.prop(props, "error_threshold")
            elif props.simplification_mode == 'CUSTOM':
                box.prop(props, "vw_tolerance", slider=True)
                box.prop(props, "error_threshold")

            box.prop(props, "show_advanced_settings")
            if props.show_advanced_settings:
                box.prop(props, "max_iterations")
                box.prop(props, "initial_learning_rate")

            # Outlier Detection
            box = layout.box()
            box.label(text="Outlier Detection:")
            box.prop(props, "use_outlier_detection")
            if props.use_outlier_detection:
                box.prop(props, "outlier_threshold", slider=True)

# --- Bone Whitelist Panel ---
class ReJemsAlterBoneWhitelistPanel(Panel):
    bl_label = "Bone Whitelist"
    bl_idname = "VIEW3D_PT_rejems_alter_bone_whitelist"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "JEMS Tools"
    bl_parent_id = "VIEW3D_PT_rejems_alter"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.rejems_alter_props
        obj = context.active_object

        # Bone selection and eyedropper
        row = layout.row()

        # Check if there is an active object and if it's an armature
        if obj and obj.type == 'ARMATURE':
            row.prop_search(props, "selected_bone_name", obj.data, "bones", text="Select Bone")
        else:
            row.label(text="Select an Armature")

        row.operator("object.rejems_alter_pick_bone", icon='EYEDROPPER', text="")

        # Add bone to whitelist
        layout.operator("object.rejems_alter_add_bone", icon='ADD', text="Add Bone to Whitelist")

        # Display whitelisted bones
        for i, item in enumerate(props.bone_whitelist):
            row = layout.row()
            row.prop(item, "name", text="", emboss=False)
            row.operator("object.rejems_alter_remove_bone", icon='REMOVE', text="").index = i