import bpy
from bpy.types import Panel

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

        layout.prop_search(props, "action_name", bpy.data, "actions", text="Select Action")

        layout.operator("object.rejems_alter")
        layout.prop(props, "use_outlier_detection")
        layout.prop(props, "outlier_threshold")
        layout.prop(props, "tolerance")
        layout.prop(props, "error_threshold")
        layout.prop(props, "max_iterations")
        layout.prop(props, "initial_learning_rate")

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

        row = layout.row()
        row.prop_search(props, "selected_bone_name", obj.data if obj and obj.type == 'ARMATURE' else None, "bones", text="Select Bone")
        row.operator("object.rejems_alter_pick_bone", icon='EYEDROPPER', text="")

        layout.operator("object.rejems_alter_add_bone", icon='ADD', text="Add Bone to Whitelist")

        for i, item in enumerate(props.bone_whitelist):
            row = layout.row()
            row.prop(item, "name", text="", emboss=False)
            row.operator("object.rejems_alter_remove_bone", icon='REMOVE', text="").index = i