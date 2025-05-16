from serial_handler import SerialHandler
from hand_tracking import hand_state_generator
import time

MAX_ANGLE = 180
MIN_ANGLE = -180

def main():
    com_port = "COM3"  # Adjust as needed
    with SerialHandler(com_port) as serial_handler:
        position = 0
        last_motor_state = None
        last_solenoid_state = None

        new_position = 0

        for motor_state, solenoid_state, motor_speed in hand_state_generator(debug=True):
            # Determine movement
            # if motor_state == "right":
            #     if position < MAX_ANGLE:
            #         position += 5  # Adjust step as needed
            #         if position > MAX_ANGLE:
            #             position = MAX_ANGLE
            #     else:
            #         motor_state = "stopped"  # Stop if limit reached
            # elif motor_state == "left":
            #     if position > MIN_ANGLE:
            #         position -= 5  # Adjust step as needed
            #         if position < MIN_ANGLE:
            #             position = MIN_ANGLE
            #     else:
            #         motor_state = "stopped"
            # else:
            #     pass  # No movement
            new_position += motor_speed
            alpha = 0.95
            position = position * (alpha) + new_position * (1.0 - alpha)


            # Only send if state changed or position changed
            if (motor_state != last_motor_state) or (solenoid_state != last_solenoid_state) or (motor_state != "stopped"):
                serial_handler.send_data(position, solenoid_state)
                print(f"Sent: position={position}, solenoid={solenoid_state}")
                last_motor_state = motor_state
                last_solenoid_state = solenoid_state

            time.sleep(0.05)


if __name__ == "__main__":
    main()
