import cv2
import numpy as np

import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as mp_drawing
import mediapipe.python.solutions.drawing_styles as mp_drawing_styles



def use_coordinates(hand_landmarks, hand_label, shape):
    # Get frame dimensions for coordinate conversion
    frame_height, frame_width, _ = shape
    
    coordinates = []    # Coordinates for finger tip landmarks

    # Process each landmark
    for landmark_id, landmark in enumerate(hand_landmarks.landmark):
        # Convert normalized coordinates to pixel values
        x_px = int(landmark.x * frame_width)
        y_px = int(landmark.y * frame_height)
        z_px = int(landmark.z * -1000)      # 1000 to get range ca. [0, 250] (forward tilt) and [-250, 0] (backward tilt)
        
        # Access and use the coordinates
        # print(f"Landmark {landmark_id}: ({x_px}, {y_px}, {landmark.z})")
        # You can also store/process these coordinates here
        
        if landmark_id == 8:
            orientation = get_palm_orientation(hand_landmarks.landmark, hand_label)
            print(f"Landmark {landmark_id}: ({x_px}, {y_px}, {z_px}). Orientation: {orientation}", end = "    \r")

        #print(get_palm_orientation(hand_landmarks.landmark))
        #coordinates.append((x_px, y_px, landmark.z))
    

def get_palm_orientation(landmarks, handedness):
    # landmarks: list of 21 MediaPipe landmarks, each with x, y, z attributes
    # Use wrist (0), index_mcp (5), pinky_mcp (17)
    wrist = np.array([landmarks[0].x, landmarks[0].y, landmarks[0].z])
    index_mcp = np.array([landmarks[5].x, landmarks[5].y, landmarks[5].z])
    pinky_mcp = np.array([landmarks[17].x, landmarks[17].y, landmarks[17].z])

    v1 = index_mcp - wrist
    v2 = pinky_mcp - wrist

    normal = np.cross(v1, v2)

    # If normal.z > 0, palm is facing camera ("front"), else "back"
    if handedness == 'Left':
        if normal[2] > 0:
            return 'Left front'
        else:
            return 'Left back'
    elif handedness == 'Right':
        if normal[2] < 0:
            return 'Right front'
        else:
            return 'Right back'
    else:
        return 'unknown'  # fallback if handedness is not provided


def run_hand_tracking_on_webcam():
    cap = cv2.VideoCapture(index=0)

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                print("Ignoring empty camera frame...")
                continue

            # Check the frame for hands
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            # Draw the hand annotations on the image
            if results.multi_hand_landmarks:

                for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    hand_label = hand_handedness.classification[0].label
                    hand_label = "Right" if hand_label == "Left" else "Left"  # Inverted labels for mirror view
                    use_coordinates(hand_landmarks, hand_label, frame.shape)
                    
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=hand_landmarks,
                        connections=mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                        connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style(),
                    )

                    break   # Only process the first hand detected

            cv2.imshow("Hand Tracking", cv2.flip(frame, 1))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()

if __name__ == "__main__":
    run_hand_tracking_on_webcam()