import asyncio
import websockets
import json
import time
from collections import defaultdict

# Globals for session data
joint_data_buffer = []
cube_position_history = []
last_cube_position = None
last_movement_time = time.time()

SESSION_TIMEOUT = 3  # seconds of cube stillness

def is_cube_still():
    if len(cube_position_history) < 2:
        return False
    pos1 = cube_position_history[-1]
    pos2 = cube_position_history[-2]
    return all(abs(a - b) < 0.001 for a, b in zip(pos1, pos2))  # precision threshold

async def handler(websocket):
    print("Client connected!")

    global last_movement_time, joint_data_buffer, cube_position_history, last_cube_position

    session_start_time = time.time()
    object_initial_position = None

    try:
        async for message in websocket:
            parts = message.strip().split(",")

            if parts[0] == "Cube":
                x, y, z, ts = map(float, parts[1:])
                cube_position = [x, y, z]
                cube_position_history.append(cube_position)

                if last_cube_position != cube_position:
                    last_cube_position = cube_position
                    last_movement_time = time.time()

                if not object_initial_position:
                    object_initial_position = cube_position

            else:
                joint_id = int(parts[0])
                px, py, pz = map(float, parts[1:4])
                rx, ry, rz, rw = map(float, parts[4:8])
                vx, vy, vz = map(float, parts[8:11])
                ts = float(parts[11])

                joint_data_buffer.append({
                    "timestamp": ts,
                    "joint_name": f"joint_{joint_id}",
                    "position": [px, py, pz],
                    "rotation": [rx, ry, rz, rw],
                    "velocity": [vx, vy, vz]
                })

            # Check if cube has been still for long enough
            if time.time() - last_movement_time > SESSION_TIMEOUT and joint_data_buffer:
                print("Cube is still — saving session data...")

                # Reorganize into frame format
                frames_by_timestamp = defaultdict(lambda: {"joints": []})
                for entry in joint_data_buffer:
                    ts = entry["timestamp"]
                    joint = {k: entry[k] for k in ["joint_name", "position", "rotation", "velocity"]}
                    frames_by_timestamp[ts]["timestamp"] = ts
                    frames_by_timestamp[ts]["joints"].append(joint)
                    frames_by_timestamp[ts]["object_position"] = last_cube_position

                session_json = {
                    "session_id": f"session_{int(session_start_time)}",
                    "user_id": "user_001",
                    "hand": "left",  # Or right depending on data source
                    "gesture_name": "unknown",
                    "start_timestamp": int(session_start_time),
                    "metadata": {
                        "recorded_on": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                        "sampling_rate_hz": 30,
                        "device": "Meta Quest 3"
                    },
                    "object": {
                        "name": "target_cube",
                        "initial_position": object_initial_position
                    },
                    "frames": list(frames_by_timestamp.values())
                }

                with open(f"session_{int(session_start_time)}.json", "w") as f:
                    json.dump(session_json, f, indent=2)

                print("Session saved. Resetting buffers...")
                joint_data_buffer.clear()
                cube_position_history.clear()
                last_cube_position = None
                session_start_time = time.time()

    except websockets.ConnectionClosed:
        print("Client disconnected.")

# Entry point
async def main():
    server = await websockets.serve(handler, "0.0.0.0", 8080)
    print("Server started on port 8080")
    await server.wait_closed()

asyncio.run(main())
