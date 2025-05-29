import cv2
from time import perf_counter
import mediapipe as mp

def run_hand_tracking_on_webcam():
    # Initialize MediaPipe components
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    mp_drawing_styles = mp.solutions.drawing_styles

    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            # Mirror and convert color space
            image = cv2.flip(image, 1)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Convert back to BGR for display
            image_rgb.flags.writeable = True
            image = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            # Process and display results
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Print landmark coordinates
                    image_height, image_width, _ = image.shape
                    for landmark_id, landmark in enumerate(hand_landmarks.landmark):
                        cx, cy = landmark.x * image_width, landmark.y * image_height
                        print(f"Landmark {landmark_id}: ({cx:.2f}, {cy:.2f})")
                    
                    # Draw annotations
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=hand_landmarks,
                        connections=mp_hands.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                        connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style()
                    )

            cv2.imshow('Hand Tracking', image)
            
            # Exit on ESC or 'q'
            key = cv2.waitKey(5)
            if key & 0xFF in (27, ord('q')):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_hand_tracking_on_webcam()

