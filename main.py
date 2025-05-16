from serial_handler import SerialHandler
from hand_tracking import hand_state_generator
import time

MAX_ANGLE = 180
MIN_ANGLE = -180

class PID:
    def __init__(self, kp, ki, kd, setpoint=0.0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.integral = 0.0
        self.last_error = 0.0

    def update(self, measurement, dt):
        error = self.setpoint - measurement
        self.integral += error * dt
        derivative = (error - self.last_error) / dt if dt > 0 else 0.0
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        self.last_error = error
        return output

def main():
    com_port = "COM3"  # Adjust as needed
    with SerialHandler(com_port) as serial_handler:
        position = 0
        last_motor_state = None
        last_solenoid_state = None

        setpoint = 0
        dt = 0
        pid = PID(kp=0.5, ki=0.0, kd=0.01, setpoint=setpoint)

        prev_time = time.time()

        for motor_state, solenoid_state, motor_speed in hand_state_generator(debug=True):
            # Update setpoint based on hand command
            setpoint += 1000 * motor_speed * dt  # motor_speed should be positive or negative step
            setpoint = max(MIN_ANGLE, min(MAX_ANGLE, setpoint))
            pid.setpoint = setpoint

            # PID control
            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time

            position += pid.update(position, dt)
            position = max(MIN_ANGLE, min(MAX_ANGLE, position))

            # Only send if state changed or position changed
            if (motor_state != last_motor_state) or (solenoid_state != last_solenoid_state) or (motor_state != "stopped"):
                serial_handler.send_data(position, solenoid_state)
                print(f"Sent: position={position:.2f}, solenoid={solenoid_state}")
                last_motor_state = motor_state
                last_solenoid_state = solenoid_state

            #time.sleep(0.05)

if __name__ == "__main__":
    main()
