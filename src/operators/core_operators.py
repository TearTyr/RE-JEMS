import bpy
import numpy as np
from ..utils import mocap_cleaning_pipeline

class ReJemsAlterOperator(bpy.types.Operator):
    bl_idname = "object.rejems_alter"
    bl_label = "Simplify Keyframes (RE:JEMS-Alter)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        props = scene.rejems_alter_props
        obj = context.active_object

        if not obj or not obj.animation_data or obj.type != 'ARMATURE':
            self.report({'WARNING'}, "Active object must be an armature with animation data.")
            return {'CANCELLED'}

        action = bpy.data.actions.get(props.action_name)

        if not action:
            self.report({'WARNING'}, "Selected action not found.")
            return {'CANCELLED'}

        new_action = bpy.data.actions.new(name=f"Simplified_{action.name}")
        new_action.use_fake_user = True

        whitelisted_bones = {item.name for item in props.bone_whitelist}

        for fcurve in action.fcurves:
            data_path_parts = fcurve.data_path.split('"')
            bone_name = data_path_parts[1] if len(data_path_parts) > 1 else ""

            if bone_name in whitelisted_bones:
                new_fcurve = new_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
                for kf in fcurve.keyframe_points:
                    new_kf = new_fcurve.keyframe_points.insert(kf.co.x, kf.co.y)
                    new_kf.interpolation = kf.interpolation
                    new_kf.handle_left = kf.handle_left
                    new_kf.handle_right = kf.handle_right
                continue

            keyframes = [(kf.co[0], kf.co[1]) for kf in fcurve.keyframe_points]

            curve, iterations, simplified_data = mocap_cleaning_pipeline(
                np.array(keyframes),
                vw_tolerance=props.tolerance,
                error_threshold=props.error_threshold,
                max_iterations=props.max_iterations,
                initial_learning_rate=props.initial_learning_rate,
                outlier_threshold=props.outlier_threshold,
                use_outlier_detection=props.use_outlier_detection
            )

            if curve:
                new_fcurve = new_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
                if simplified_data is not None:
                    for i in range(len(simplified_data)):
                        frame, value = simplified_data[i]
                        kf = new_fcurve.keyframe_points.insert(frame, value)
                        kf.interpolation = 'BEZIER'

                        if i > 0:
                            kf.handle_left = (
                                simplified_data[i - 1][0] + (frame - simplified_data[i - 1][0]) / 3,
                                simplified_data[i - 1][1] + (value - simplified_data[i - 1][1]) / 3
                            )
                        else:
                            kf.handle_left_type = 'AUTO'

                        if i < len(simplified_data) - 1:
                            kf.handle_right = (
                                frame + (simplified_data[i + 1][0] - frame) / 3,
                                value + (simplified_data[i + 1][1] - value) / 3
                            )
                        else:
                            kf.handle_right_type = 'AUTO'

        obj.animation_data.action = new_action
        self.report({'INFO'}, f"Simplified action created: {new_action.name}")
        return {'FINISHED'}