import cv2
import numpy as np
#import RPi.GPIO as GPIO
import time
import mediapipe as mp

# GPIO setup
MOTOR_DIR_PIN = 17
MOTOR_STEP_PIN = 27
SOLENOID_PIN = 22

#GPIO.setmode(#GPIO.BCM)
#GPIO.setup(MOTOR_DIR_PIN, #GPIO.OUT)
#GPIO.setup(MOTOR_STEP_PIN, #GPIO.OUT)
#GPIO.setup(SOLENOID_PIN, #GPIO.OUT)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def calculate_angle(v1, v2):
    unit_v1 = v1 / np.linalg.norm(v1)
    unit_v2 = v2 / np.linalg.norm(v2)
    dot = np.clip(np.dot(unit_v1, unit_v2), -1.0, 1.0)
    angle = np.arccos(dot)
    return np.degrees(angle)

def map_range(value, from_min, from_max, to_min, to_max):
    value = max(min(value, from_max), from_min)
    return to_min + (value - from_min) * (to_max - to_min) / (from_max - from_min)

def step_motor(steps, delay=0.002):
    for _ in range(steps):
        #GPIO.output(MOTOR_STEP_PIN, #GPIO.HIGH)
        time.sleep(delay)
        #GPIO.output(MOTOR_STEP_PIN, #GPIO.LOW)
        time.sleep(delay)

def run():
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
        motor_running = False
        solenoid_on = False

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            if results.multi_hand_landmarks:
                landmarks = results.multi_hand_landmarks[0].landmark

                wrist = np.array([landmarks[0].x, landmarks[0].y])
                middle_tip = np.array([landmarks[12].x, landmarks[12].y])
                middle_mcp = np.array([landmarks[9].x, landmarks[9].y])

                v1 = middle_mcp - wrist
                v2 = middle_tip - wrist

                angle = calculate_angle(v1, v2)

                # Motor control logic
                if angle < 150:
                    #GPIO.output(MOTOR_DIR_PIN, #GPIO.HIGH)  # Set motor direction
                    step_motor(10)  # Step motor 10 pulses
                    if not motor_running:
                        print("Motor started")
                    motor_running = True
                else:
                    if motor_running:
                        print("Motor stopped")
                    motor_running = False

                # Solenoid control logic
                dist = np.linalg.norm(middle_tip - wrist)
                threshold = 0.05

                if dist < threshold and not solenoid_on:
                    #GPIO.output(SOLENOID_PIN, #GPIO.HIGH)
                    solenoid_on = True
                    print("Solenoid activated")
                elif dist >= threshold and solenoid_on:
                    #GPIO.output(SOLENOID_PIN, #GPIO.LOW)
                    solenoid_on = False
                    print("Solenoid deactivated")

                # Draw landmarks and info
                mp_drawing.draw_landmarks(frame, results.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
                cv2.putText(frame, f"Motor: {'Running' if motor_running else 'Stopped'}", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Solenoid: {'ON' if solenoid_on else 'OFF'}", (10, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # No hand detected - stop motor and solenoid
                if motor_running:
                    print("Motor stopped (no hand detected)")
                if solenoid_on:
                    print("Solenoid deactivated (no hand detected)")
                motor_running = False
                solenoid_on = False
                #GPIO.output(SOLENOID_PIN, #GPIO.LOW)

            cv2.imshow("Hand Motor Control", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()
    #GPIO.cleanup()


if __name__ == "__main__":
    run()
