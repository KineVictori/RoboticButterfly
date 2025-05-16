import serial
from typing import Optional

class SerialHandler:
    def __init__(self, com_port: str, baudrate: int = 115200, timeout: float = 1.0):
        self.ser: Optional[serial.Serial] = None
        try:
            self.ser = serial.Serial(com_port, baudrate, timeout=timeout)
            print(f"Serial port {com_port} opened at {baudrate} baud.")
        except serial.SerialException as e:
            print(f"Failed to open serial port {com_port}: {e}")

    def send_data(self, position: float, solenoid_strength: int):
        if self.ser and self.ser.is_open:
            msg = f"{position},{solenoid_strength}\n"
            self.ser.write(msg.encode())
        else:
            print("Serial port not open. Cannot send data.")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("Serial port closed.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
