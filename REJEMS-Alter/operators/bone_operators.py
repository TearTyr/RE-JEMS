import bpy
from bpy.types import Operator
from bpy.props import IntProperty

# --- Operator to Pick Bone with Eyedropper ---
class ReJemsAlterPickBoneOperator(Operator):
    bl_idname = "object.rejems_alter_pick_bone"
    bl_label = "Pick Bone"
    bl_description = "Pick a bone to add to the whitelist"

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Get the selected bone
            selected_bone = context.active_pose_bone
            if selected_bone:
                context.scene.rejems_alter_props.selected_bone_name = selected_bone.name
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, "No bone selected.")
                return {'CANCELLED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}

# --- Operator to Add Bone to Whitelist ---
class ReJemsAlterAddBoneOperator(Operator):
    bl_idname = "object.rejems_alter_add_bone"
    bl_label = "Add Bone to Whitelist"
    bl_description = "Add the selected bone to the whitelist"

    def execute(self, context):
        scene = context.scene
        props = scene.rejems_alter_props
        bone_name = props.selected_bone_name

        if not bone_name:
            self.report({'WARNING'}, "No bone selected.")
            return {'CANCELLED'}

        if any(item.name == bone_name for item in props.bone_whitelist):
            self.report({'WARNING'}, "Bone already in whitelist.")
            return {'CANCELLED'}

        item = props.bone_whitelist.add()
        item.name = bone_name
        return {'FINISHED'}

# --- Operator to Remove Bone from Whitelist ---
class ReJemsAlterRemoveBoneOperator(Operator):
    bl_idname = "object.rejems_alter_remove_bone"
    bl_label = "Remove Bone from Whitelist"
    bl_description = "Remove the selected bone from the whitelist"

    index: IntProperty()

    def execute(self, context):
        scene = context.scene
        props = scene.rejems_alter_props
        props.bone_whitelist.remove(self.index)
        return {'FINISHED'}