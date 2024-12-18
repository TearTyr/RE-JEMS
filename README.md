# RE:JEMS-Alter: Blender Add-on for Animation Keyframe Simplification

## Overview

**RE:JEMS-Alter** is a Blender add-on designed to simplify animation keyframes, resulting in smoother animations and smaller file sizes. It utilizes a **Bezier curve fitting algorithm** that intelligently adjusts control points to fit a curve to the original keyframe data. The algorithm adapts to the number of input points, effectively providing the functionality of Visvalingam-Whyatt within the curve fitting process.

RE:JEMS-Alter also provides an option to use the Visvalingam-Whyatt algorithm for initial keyframe reduction, and it includes an outlier detection mechanism to enhance the robustness of the simplification process. You can control the degree of simplification through various parameters, making it a versatile tool for animators.

**Note:** The name "JEMS" in RE:JEMS-Alter is not an acronym but simply a name chosen for this project.

## Features

*   **Bezier Curve Fitting Algorithm:** Efficiently simplifies keyframes by fitting a Bezier curve to the animation data.
*   **Visvalingam-Whyatt Simplification:** Option to pre-process keyframes using the Visvalingam-Whyatt algorithm for initial reduction.
*   **Outlier Detection:** Identifies and optionally removes outlier keyframes to improve fitting accuracy.
*   **Bone Whitelist:** Exclude specific bones from simplification, preserving their original animation data.
*   **Adjustable Parameters:** Fine-tune the simplification process with parameters like:
    *   **VW Tolerance:** Controls the simplification level of the Visvalingam-Whyatt algorithm.
    *   **Error Threshold:** Determines the desired accuracy of the Bezier curve fit.
    *   **Max Iterations:** Sets the maximum number of iterations for the algorithm.
    *   **Initial Learning Rate:** Controls the initial step size for control point adjustments.
    *   **Outlier Threshold:** Sets the sensitivity for outlier detection.
*   **User-Friendly UI:** Integrates seamlessly into Blender's UI with a dedicated panel in the 3D View sidebar.

## Installation

1. **Download the Repository:** Download the RE:JEMS-Alter repository as a ZIP file and extract it to a suitable location on your computer.
2. **Run `zip_addon.bat`:** Navigate to the root directory of the extracted repository (the `rejems_alter_project` folder) and double-click the `zip_addon.bat` script. This will create a `rejems_alter.zip` file in the `output` folder.
3. **Install in Blender:**

    *   Open Blender and go to **Edit > Preferences > Add-ons**.
    *   Click the **Install** button.
    *   Navigate to the `output` directory inside the `rejems_alter_project` folder, select the `rejems_alter.zip` file, and click **Install Add-on**.
4. **Enable the Add-on:** Check the box next to **"RE:JEMS-Alter"** in the add-on list.

## Usage

1. **Select an Armature Object:** Ensure that the active object is an armature with animation data.
2. **Choose an Action:** In the RE:JEMS-Alter panel (found in the 3D View sidebar under the "JEMS Tools" tab), select the animation action you want to simplify from the "Select Action" dropdown.
3. **Adjust Parameters (Optional):**

    *   **Use Outlier Detection:** Toggle outlier detection on or off.
    *   **Outlier Threshold:** Adjust the sensitivity of the outlier detection.
    *   **VW Tolerance:** Set the desired tolerance for Visvalingam-Whyatt simplification (if used).
    *   **Error Threshold:** Modify the target accuracy for the Bezier curve fit.
    *   **Max Iterations:** Change the maximum number of iterations for the algorithm.
    *   **Initial Learning Rate:** Fine-tune the initial learning rate.
4. **Manage Bone Whitelist (Optional):**

    *   Go to the "Bone Whitelist" subpanel.
    *   Use the eyedropper to select bones in the 3D viewport or manually type their names.
    *   Add bones to the whitelist to prevent them from being simplified.
5. **Simplify Keyframes:** Click the "Simplify Keyframes (RE:JEMS-Alter)" button.
6. **New Action Created:** A new action named "Simplified\_\<original action name\>" will be created and assigned to the armature. This new action contains the simplified keyframes.

## How It Works

The RE:JEMS-Alter add-on employs a multi-stage pipeline for keyframe simplification:

1. **Outlier Detection (Optional):** If enabled, the add-on detects and removes outlier keyframes using a median-based approach.
2. **Visvalingam-Whyatt Simplification (Optional):** If a VW Tolerance is specified, the Visvalingam-Whyatt algorithm reduces the number of keyframes based on their contribution to the overall shape of the animation curve.
3. **Bezier Curve Fitting:**

    *   The algorithm initializes control points for a Bezier curve, potentially using the simplified points from the previous step or directly from the original keyframes if no simplification is applied.
    *   It iteratively adjusts these control points to minimize the error between the generated Bezier curve and the original (or simplified) keyframe data.
    *   The number of points at which the Bezier curve is evaluated (t-values) is dynamically adjusted based on the number of input points, effectively integrating a Visvalingam-Whyatt-like approach into the fitting process.
    *   The algorithm stops when the maximum error falls below the specified error threshold or the maximum number of iterations is reached.
4. **Keyframe Placement and Handle Adjustment:** New keyframes are placed based on the simplified data, and Bezier handles are adjusted to approximate the shape of the fitted curve.

## Notes

*   The original animation action is preserved. RE:JEMS-Alter creates a new action with the simplified keyframes.
*   The add-on is designed for armatures with animation data. Using it on other object types may not produce the desired results.
*   Experiment with the parameters to achieve the best balance between simplification and accuracy for your specific animation.
*   If you have many bones that you don't want simplified, adding them to the whitelist can significantly improve performance by preventing unnecessary calculations.

## License and Attribution

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**Attribution is required if you use or distribute this add-on.** 

You must clearly state that the add-on was created by:

*   **TearTyr / L / Meri**

Please include a link to the original repository or project page if available.

If you modify the add-on, you must indicate that changes were made and provide attribution to the original authors.

## Authors

*   TearTyr / L / Meri

## Version

1.2.8

## Blender Compatibility

Blender 4.0+ and later.