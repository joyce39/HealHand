import json
import math
import numpy as np
import pandas as pd

def euclidean_distance(a, b):
    return math.sqrt(sum((ai - bi) ** 2 for ai, bi in zip(a, b)))

def compare_sessions(baseline_path, test_path):
    with open(baseline_path, 'r') as f:
        baseline = json.load(f)
    with open(test_path, 'r') as f:
        test = json.load(f)

    frame_count = min(len(baseline['frames']), len(test['frames']))
    joint_names = {joint['joint_name'] for frame in baseline['frames'][:frame_count] for joint in frame['joints']}

    joint_stats = {}

    for joint_name in joint_names:
        pos_diffs = []
        vel_diffs = []

        for i in range(frame_count):
            base_frame = baseline['frames'][i]
            test_frame = test['frames'][i]

            # Get wrist joints
            base_wrist = next((j for j in base_frame['joints'] if j['joint_name'] == 'wrist'), None)
            test_wrist = next((j for j in test_frame['joints'] if j['joint_name'] == 'wrist'), None)
            if not base_wrist or not test_wrist:
                continue

            # Get the joint we're comparing
            base_joint = next((j for j in base_frame['joints'] if j['joint_name'] == joint_name), None)
            test_joint = next((j for j in test_frame['joints'] if j['joint_name'] == joint_name), None)
            if not base_joint or not test_joint:
                continue

            # Normalize positions to wrist
            base_pos = [a - b for a, b in zip(base_joint['position'], base_wrist['position'])]
            test_pos = [a - b for a, b in zip(test_joint['position'], test_wrist['position'])]

            pos_diff = euclidean_distance(test_pos, base_pos)
            pos_diffs.append(pos_diff)

            # Velocity stays unchanged (world space comparison for now)
            vel_diff = euclidean_distance(test_joint['velocity'], base_joint['velocity'])
            vel_diffs.append(vel_diff)

        if pos_diffs:
            joint_stats[joint_name] = {
                'avg_position_offset_m': round(float(np.mean(pos_diffs)), 5),
                'max_position_offset_m': round(float(np.max(pos_diffs)), 5),
                'position_offset_stddev_m': round(float(np.std(pos_diffs)), 5),
                'max_velocity_difference_mps': round(float(np.max(vel_diffs)), 5)
            }

    return joint_stats  # now returns a dictionary (not a DataFrame)

if __name__ == "__main__":
    baseline_file = "baseline_shifted.json"
    test_file = "test_shifted.json"

    joint_summary = compare_sessions(baseline_file, test_file)

    # Convert to JSON string for chatbot
    print(json.dumps(joint_summary, indent=2))
