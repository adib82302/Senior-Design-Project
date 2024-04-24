import time
import board
import busio
import adafruit_pca9685
from adafruit_servokit import ServoKit
import serial
import adafruit_bno055
import csv

# Setup for PWM, serial, and I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize devices with explicit addresses
hat = adafruit_pca9685.PCA9685(i2c, address=0x40)  # Address for PCA9685
kit = ServoKit(channels=16, i2c=i2c, address=0x40)  # Same address as PCA9685, handled by ServoKit
sensor = adafruit_bno055.BNO055_I2C(i2c, address=0x28)  # Default address for BNO055

# Initialize serial connection
ser = serial.Serial('/dev/ttyAMA2', 115200)  # Ensure to match your device port and baud rate

# Motor channels
left_channel = 15
right_channel = 14

# Movement functions
def forward():
    kit.continuous_servo[left_channel].throttle = 0.3
    kit.continuous_servo[right_channel].throttle = 0.3

def stop():
    kit.continuous_servo[left_channel].throttle = 0
    kit.continuous_servo[right_channel].throttle = 0

def turn_around():
    kit.continuous_servo[left_channel].throttle = -0.3
    kit.continuous_servo[right_channel].throttle = 0.3
    time.sleep(1)  # Adjust time for a 180 turn
    stop()

# Distance sensing
def read_distance():
    ser.write(bytes([0x55]))
    time.sleep(0.1)
    if ser.inWaiting() > 0 and ser.read(1)[0] == 0xFF:
        buffer = [0xFF] + [ord(ser.read(1)) for _ in range(3)]
        if buffer[3] == sum(buffer[:3]) & 0xFF:
            return (buffer[1] << 8) + buffer[2]
    return None

# Main routine
try:
    forward()
    while True:
        distance = read_distance()
        if distance and distance < 50:  # Stop if closer than 50 cm
            stop()
            turn_around()
            forward()
            break
    time.sleep(5)  # Adjust time for return journey
    stop()

    # Record data to CSV
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['X', 'Y', 'Z'])
        accel = sensor.acceleration
        writer.writerow(accel if accel else [0, 0, 0])

except KeyboardInterrupt:
    print("Stopped by user")
finally:
    ser.close()
