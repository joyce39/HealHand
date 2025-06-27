# HealHand
HealHand is a Mixed Reality assitive AI powered rehab assistant based on ADLs

Project Overview
Developed in Unity 2022.3.5f1


Built on top of the Meta Passthrough Multi-Object Detection Sample

Key features:


- Realtime object detection on headset running yolov9
- Hand tracking and gesture monitoring
- Voice and visual feedback using an adaptive virtual coach
- Realtime JSON data transmission via WebSocket
- Feedback generation through LLM-based analysis


Unity Project Structure:

It can be found in the HealHand unity zip on drive because of folder size constraints.

Main Scene: HandOD
 Found at: Assets > PassthroughCameraApiSamples > MultiObjectDetection


Core folder: ADL
 Contains:
- Custom scripts
- Prefabs (ghost hand, orbs, objects of daily living)
- Animations and state machines
- Audio clips for feedback
- Main prefabs & components:
- DetectionManagerPrefab: main logic container
- CustomDetectionManager_unified.cs: handles flow logic, audio cues, object spawning, adaptive responses
- WebCamTextureManager: provides real-time video for detection
- HandTracker + OVRSkeleton: streams hand tracking data
- JointStreamer: sends joint data over WebSocket
- Audio_clips: demo voice files for virtual therapist
- AnimatorControllers: used for ghost hand guidance



Setting Up the HandOD Scene:
1. Duplicate Base Scene
Start with the MultiObjectDetection scene 
2. Add Grabbable Object
Insert any 3D object (e.g., a building block) and ensure:
XR Interaction Toolkit is enabled
3. Attach Detection Logic
Add CustomDetectionManager_unified.cs to the DetectionManagerPrefab.
4. Assign Dependencies in Inspector
Drag in:
WebCamTextureManager
Hand Prefab
Marker Prefab
Sentis components for model inference
5. Enable Hand Tracking and websocket communication if needed
Ensure hand tracking is enabled in XR Settings for Meta Quest.

-Python (PC) Side – AI Coach Scripts
Found in the AI_coach_scripts folder.

1. json_hand_data_server.py
Launches a WebSocket server
Receives and formats live hand tracking data into JSON


2. joint_comparison_normalized.py
Takes the captured JSON file
Computes metrics (offsets, velocity difference)
Outputs a new JSON with performance stats


3. chatbot.py
Loads the metrics output
ses LLM to generate feedback and engage in dialogue
emulates a supportive therapist with patient-friendly guidance

LLM model used:
Model name: Chocolatine-3B-Instruct-DPO-v1.2


Sourced from Hugging Face: Chocolatine on Hugging Face


By default, chatbot.py will:
Automatically download the model from Hugging Face the first time it's used


The folder includees sample baseline and testing files of gesture trajectories for testing purposes.
