import serial
 
class SerialHandler:
    def __init__(self, comNum):
        self.ser = serial.Serial(f"COM{comNum}", 115200, timeout=1)
   
    def sendData(self, position, solenoidStrenght):
        """
        Takes in a position in degrees. Example '128.3' or '-789.134'
        Takes in soleniodStrenght in range [0, 255]
        """
 
        msg = f"{position},{solenoidStrenght}\n"
        self.ser.write(msg.encode())
   
    def __del__(self):
        self.ser.close()
 

def main():
    serialHandler = SerialHandler(3)
 
    while True:
        message = input(">")
        if message == "":
            break
 
        x, y = message.split(",")
 
        serialHandler.sendData(float(x), float(y))
 
if __name__ == "__main__":
    main()