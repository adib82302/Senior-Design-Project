import serial
import time

# Define serial port
ser = serial.Serial('/dev/ttyS0', 115200)  # Assuming you're using the Raspberry Pi's UART

# Define constants
COM = 0x55

def calculate_checksum(data):
    return sum(data) & 0xFF

def read_sensor():
    # Write command to sensor
    ser.write(bytes([COM]))
    time.sleep(0.1)  # Wait for sensor to respond
    
    if ser.in_waiting > 0:
        # Read response
        response = ser.read(1)
        
        if response[0] == 0xFF:
            buffer_RTT = [0xFF]
            buffer_RTT.extend(ser.read(3))
            
            # Calculate checksum
            CS = sum(buffer_RTT[:-1]) & 0xFF
            
            # Verify checksum
            if buffer_RTT[3] == CS:
                # Extract distance data
                Distance = (buffer_RTT[1] << 8) + buffer_RTT[2]
                print("Distance:", Distance, "mm")

if __name__ == "__main__":
    try:
        ser.open()
        print("Serial port opened successfully")
        
        while True:
            read_sensor()
            time.sleep(0.1)  # Adjust delay as needed
            
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()
