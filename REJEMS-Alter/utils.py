import numpy as np
from math import comb

class BezierCurve:
    """Represents a Bezier curve of any given degree."""
    def __init__(self, control_points: np.ndarray):
        self.control_points = np.array(control_points)
        self.degree = len(control_points) - 1

    def point(self, t):
        n = self.degree
        point = np.zeros(self.control_points.shape[1])
        for i in range(n + 1):
            bernstein_coeff = comb(n, i) * (t ** i) * ((1 - t) ** (n - i))
            point += bernstein_coeff * self.control_points[i]
        return point

    def evaluate_multi(self, t_values):
        points = np.array([self.point(t) for t in t_values])
        return points

def get_initial_control_points(points: np.ndarray, vw_tolerance=None):
    """
    Initializes control points using simplified points from Visvalingam-Whyatt or directly
    from input points.
    """
    points = np.array(points)
    simplified_points = points

    if vw_tolerance:
        simplified_points = visvalingam_whyatt(points, vw_tolerance)

    return simplified_points

def initial_control_points_heuristic(points, vw_tolerance=None):
    """
    Initializes control points using simplified points from Visvalingam-Whyatt.
    The degree is determined by the simplified points.
    """
    points = np.array(points)
    simplified_points = points

    if vw_tolerance:
        simplified_points = visvalingam_whyatt(points, vw_tolerance)

    return simplified_points

def detect_outliers(points, threshold=3):
    """
    Detects outliers using a median-based approach with special handling for edges.
    """
    outliers = np.zeros(len(points), dtype=bool)
    if len(points) < 3:
        return outliers

    # Handle first and last points separately
    if np.linalg.norm(points[0] - points[1]) > threshold:
        outliers[0] = True
    if np.linalg.norm(points[-1] - points[-2]) > threshold:
        outliers[-1] = True

    # Use median for central points
    for i in range(1, len(points) - 1):
        prev_point = points[i - 1]
        current_point = points[i]
        next_point = points[i + 1]

        # Calculate the median point
        median_point = np.median([prev_point, next_point], axis=0)

        # Calculate the deviation from the median point
        deviation = np.linalg.norm(current_point - median_point)

        # Mark as outlier if deviation is above the threshold
        if deviation > threshold:
            outliers[i] = True
    return outliers

def adaptive_jems_algorithm(points: np.ndarray, error_threshold: float=0.05, max_iterations: int=100, initial_learning_rate: float=0.2, convergence_window: int=5):
    """
    JEMS algorithm that adapts to the number of input points, similar to VW.
    It generates t_values based on the number of input points.
    """
    points = np.array(points)
    control_points = get_initial_control_points(points)
    bezier_degree = len(control_points) - 1
    num_points = len(points)

    if num_points < bezier_degree + 1:
        print(f"Not enough points ({num_points}) to fit a Bezier curve with {bezier_degree} degree.")
        return None, 0

    # Generate t_values and corresponding indices in the data points array
    num_t_values = max(100, num_points * 2)
    t_values = np.linspace(0, 1, num_t_values)
    t_values_to_fit = np.linspace(0, num_points - 1, num_t_values, dtype=int)

    curve = BezierCurve(control_points)
    previous_errors = []

    for iteration in range(max_iterations):
        learning_rate = initial_learning_rate * (0.99 ** iteration)

        curve_points = curve.evaluate_multi(t_values)

        # --- More Vectorized Error Calculation ---
        distances = np.linalg.norm(curve_points - points[t_values_to_fit], axis=1)
        # ------------------------------------------

        max_error = np.max(distances)
        average_error = np.mean(distances)
        previous_errors.append(average_error)

        # Convergence check
        if max_error <= error_threshold:
            if len(previous_errors) > convergence_window:
                error_range = np.max(previous_errors[-convergence_window:]) - np.min(previous_errors[-convergence_window:])
                if error_range < error_threshold / 10:
                    print(f"Adaptive JEMS converged after {iteration+1} iterations with max error {max_error:.4f} and average error {average_error:.4f}.")
                    return curve, iteration
            else:
                print(f"Adaptive JEMS converged after {iteration+1} iterations with max error {max_error:.4f} and average error {average_error:.4f}.")
                return curve, iteration

        # Convergence based on error change
        if len(previous_errors) > convergence_window:
            error_range = np.max(previous_errors[-convergence_window:]) - np.min(previous_errors[-convergence_window:])
            if error_range < error_threshold / 10 and max_error <= error_threshold:
                print(f"Adaptive JEMS converged based on error change after {iteration+1} iterations, max error: {max_error:.4f}, avg error: {average_error:.4f}")
                return curve, iteration

        # --- More Vectorized Control Point Adjustment ---
        max_error_index = np.argmax(distances)

        # Calculate basis values for all control points at once
        basis_values = np.array([comb(bezier_degree, i) * (t_values[max_error_index] ** i) * ((1 - t_values[max_error_index]) ** (bezier_degree - i)) for i in range(bezier_degree + 1)])

        # Calculate error vector
        error_vector = (points[t_values_to_fit][max_error_index] - curve_points[max_error_index])

        # Vectorized adjustment calculation and update
        adjustment_vector = learning_rate * basis_values[:, np.newaxis] * error_vector
        control_points += np.clip(adjustment_vector, -0.5, 0.5)
        # --------------------------------------------------

        curve = BezierCurve(control_points)

    print(f"Adaptive JEMS did not converge within {max_iterations} iterations. Max error: {max_error:.4f}, Avg error: {average_error:.4f}")
    return curve, iteration

def visvalingam_whyatt(points: np.ndarray, tolerance: float):
    if len(points) < 3:
        return np.array(points)

    def triangle_area(p1, p2, p3):
        return 0.5 * np.abs((p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1]))

    simplified_points = list(points)
    areas = []
    for i in range(1, len(simplified_points) - 1):
        areas.append((triangle_area(simplified_points[i-1], simplified_points[i], simplified_points[i+1]), i))

    while areas and min(areas)[0] < tolerance:
        min_area, index_to_remove = min(areas)
        del simplified_points[index_to_remove]
        areas = []
        if len(simplified_points) > 2:
            for i in range(1, len(simplified_points) - 1):
                areas.append((triangle_area(simplified_points[i-1], simplified_points[i], simplified_points[i+1]), i))
        else:
            break

    return np.array(simplified_points)

def mocap_cleaning_pipeline(mocap_data: np.ndarray, vw_tolerance:float=None, error_threshold:float=0.05, max_iterations:int=100, initial_learning_rate:float=0.2, outlier_threshold:float=3, use_outlier_detection:bool=True):
    """
    A pipeline for cleaning mocap data using outlier detection and Bezier curve fitting.

    Args:
        mocap_data (np.ndarray): The raw mocap data points.
        vw_tolerance (float, optional): Tolerance for Visvalingam-Whyatt simplification. Defaults to None (no simplification).
        error_threshold (float, optional): Error threshold for JEMS convergence. Defaults to 0.05.
        max_iterations (int, optional): Maximum iterations for JEMS. Defaults to 100.
        learning_rate (float, optional): Learning rate for JEMS. Defaults to 0.2.
        outlier_threshold (float, optional): Threshold for outlier detection. Defaults to 3.
        use_outlier_detection (bool, optional): Enable or disable outlier detection. Defaults to True.

    Returns:
        tuple: The fitted Bezier curve object and the number of iterations, or None and 0 if fitting fails.
    """
    try:
        # 1. Detect and potentially remove outliers
        if use_outlier_detection:
            outlier_indices = detect_outliers(mocap_data, threshold=outlier_threshold)
            cleaned_data = np.delete(mocap_data, outlier_indices, axis=0)
            print(f"Detected {outlier_indices.sum()} outliers.")
        else:
            cleaned_data = mocap_data

        if len(cleaned_data) < 2:
            print("Not enough points after outlier removal to fit a Bezier curve of this degree.")
            return None, 0

        # 2. Apply Visvalingam-Whyatt simplification if a tolerance is provided
        if vw_tolerance is not None:
            simplified_data = visvalingam_whyatt(cleaned_data, vw_tolerance)
            print(f"Simplified data from {len(cleaned_data)} to {len(simplified_data)} points using Visvalingam-Whyatt.")
            if len(simplified_data) < 2:
                print("Not enough points after simplification to fit a Bezier curve of this degree.")
                return None, 0
            curve, iterations = adaptive_jems_algorithm(simplified_data, error_threshold, max_iterations, initial_learning_rate)
            return curve, iterations, simplified_data
        else:
            curve, iterations = adaptive_jems_algorithm(cleaned_data, error_threshold, max_iterations, initial_learning_rate)
            return curve, iterations, cleaned_data
    except Exception as e:
        print(f"An error occurred in the mocap_cleaning_pipeline: {e}")
        return None, 0, None