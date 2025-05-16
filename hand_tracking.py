import cv2
import numpy as np
import mediapipe.python.solutions.hands as mp_hands


def hand_state_generator(debug=False):
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        model_complexity=0,
        max_num_hands=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
    ) as hands:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                continue

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            motor_state = "stopped"
            solenoid_state = 0
            motor_speed = 0.0

            if results.multi_hand_landmarks and results.multi_handedness:
                landmarks = results.multi_hand_landmarks[0].landmark
                hand_label = results.multi_handedness[0].classification[0].label  # "Left" or "Right"

                wrist = landmarks[0]
                middle_tip = landmarks[12]
                horizontal_diff = middle_tip.x - wrist.x
                dx = middle_tip.x - wrist.x
                dy = middle_tip.y - wrist.y
                distance = np.sqrt(dx**2 + dy**2)
                
                threshold = 0.02  # or your preferred threshold

                # Solenoid logic
                solenoid_state = 255 if distance < 0.15 else 0

                # Motor direction logic
                horizontal_diff = middle_tip.x - wrist.x
                threshold = 0.05
                
                # Flip direction for right hand
                if hand_label == "Right":
                    horizontal_diff = -horizontal_diff  # Mirror the X-axis

                motor_speed = horizontal_diff

                if horizontal_diff > threshold:
                    motor_state = "right"
                elif horizontal_diff < -threshold:
                    motor_state = "left"
                else:
                    motor_state = "stopped"

            yield motor_state, solenoid_state, motor_speed
            

            if debug:
                import mediapipe.python.solutions.drawing_utils as mp_drawing
                import mediapipe.python.solutions.drawing_styles as mp_drawing_styles
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            frame,
                            hand_landmarks,
                            mp_hands.HAND_CONNECTIONS,
                            mp_drawing_styles.get_default_hand_landmarks_style(),
                            mp_drawing_styles.get_default_hand_connections_style()
                        )
                cv2.imshow("Hand Tracking", cv2.flip(frame, 1))
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

    cap.release()
    cv2.destroyAllWindows()
