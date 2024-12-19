import bpy
import numpy as np
from ..utils import BezierCurve, mocap_cleaning_pipeline
from bpy.types import Operator

# --- Operator to Simplify Keyframes ---
class ReJemsAlterOperator(Operator):
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

        # Create a set of whitelisted bone names for faster lookup
        whitelisted_bones = {item.name for item in props.bone_whitelist}

        for fcurve in action.fcurves:
            # Check if the bone associated with this fcurve is whitelisted
            data_path_parts = fcurve.data_path.split('"')
            if len(data_path_parts) > 1:
                bone_name = data_path_parts[1]
            else:
                bone_name = ""

            if bone_name in whitelisted_bones:
                # Copy the original fcurve to the new action without modification
                new_fcurve = new_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)
                for kf in fcurve.keyframe_points:
                    new_kf = new_fcurve.keyframe_points.insert(kf.co.x, kf.co.y)
                    new_kf.interpolation = kf.interpolation
                    new_kf.handle_left = kf.handle_left
                    new_kf.handle_right = kf.handle_right
                continue  # Skip to the next fcurve

            keyframes = [(kf.co[0], kf.co[1]) for kf in fcurve.keyframe_points]

            # Determine parameters based on simplification mode
            # (No changes needed here - we're changing the UI values instead)
            if props.simplification_mode == 'BALANCED':
                vw_tol = props.vw_tolerance
                err_thresh = 0.05
            elif props.simplification_mode == 'ACCURATE':
                vw_tol = None  # No VW simplification
                err_thresh = props.error_threshold
            else:  # CUSTOM
                vw_tol = props.vw_tolerance
                err_thresh = props.error_threshold

            curve, iterations, simplified_data = mocap_cleaning_pipeline(
                np.array(keyframes),
                vw_tolerance=vw_tol,
                error_threshold=err_thresh,
                max_iterations=props.max_iterations,
                initial_learning_rate=props.initial_learning_rate,
                outlier_threshold=props.outlier_threshold,
                use_outlier_detection=props.use_outlier_detection
            )

            if curve:
                new_fcurve = new_action.fcurves.new(data_path=fcurve.data_path, index=fcurve.array_index)

                # Use simplified data for keyframe placement and initial handle positions
                if simplified_data is not None:
                    for i in range(len(simplified_data)):
                        frame = simplified_data[i][0]
                        value = simplified_data[i][1]

                        # Insert keyframe
                        kf = new_fcurve.keyframe_points.insert(frame, value)
                        kf.interpolation = 'BEZIER'

                        # Set initial handle positions based on neighboring points
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