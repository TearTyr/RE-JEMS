import bpy
from bpy.types import Operator

# --- Operator to Pick Action with Eyedropper ---
class ReJemsAlterPickActionOperator(Operator):
    bl_idname = "object.rejems_alter_pick_action"
    bl_label = "Pick Action"
    bl_description = "Pick an action using the eyedropper"

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            # Get the selected object
            obj = context.object
            if obj and obj.animation_data and obj.animation_data.action:
                context.scene.rejems_alter_props.action_name = obj.animation_data.action.name
                return {'FINISHED'}
            else:
                self.report({'WARNING'}, "Selected object does not have an action.")
                return {'CANCELLED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}