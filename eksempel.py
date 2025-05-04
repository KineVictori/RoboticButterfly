import cv2

from time import perf_counter

import mediapipe.python.solutions.hands as mp_hands
import mediapipe.python.solutions.drawing_utils as mp_drawing
import mediapipe.python.solutions.drawing_styles as mp_drawing_styles



def use_coordinates(hand_landmarks, shape):
    # Get frame dimensions for coordinate conversion
    frame_height, frame_width, _ = shape
    
    # Process each landmark
    for landmark_id, landmark in enumerate(hand_landmarks.landmark):
        # Convert normalized coordinates to pixel values
        x_px = int(landmark.x * frame_width)
        y_px = int(landmark.y * frame_height)
        
        # Access and use the coordinates
        print(f"Landmark {landmark_id}: ({x_px}, {y_px})")
        # You can also store/process these coordinates here
        
        if landmark_id == 8:
            print("Fant 8!")





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
                use_coordinates(results.multi_hand_landmarks[0], frame_rgb.shape)

                for hand_landmarks in results.multi_hand_landmarks:
                    
                    
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=hand_landmarks,
                        connections=mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                        connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style(),
                    )

                    break

            cv2.imshow("Hand Tracking", cv2.flip(frame, 1))
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cap.release()

if __name__ == "__main__":
    run_hand_tracking_on_webcam()