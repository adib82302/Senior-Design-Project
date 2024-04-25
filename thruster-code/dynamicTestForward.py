import time
import board
import busio
import adafruit_pca9685


# Initialize I2C bus and PCA9685 object
i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

from adafruit_servokit import ServoKit
kit = ServoKit(channels=16)

# Define PCA9685 channels for left and right motors
left_channel = 15
right_channel = 14
left_v_channel = 13
right_v_channel = 12

# Set  pulse width range for both motors
kit.continuous_servo[left_channel].throttle = 0.1
kit.continuous_servo[right_channel].throttle = 0.1
kit.continuous_servo[left_v_channel].throttle = 0.1
kit.continuous_servo[right_v_channel].throttle = 0.1

time.sleep(5)

def forward():
  initial_left = 0.3
  initial_right = 0.3
  kit.continuous_servo[left_channel].throttle = initial_left
  kit.continuous_servo[right_channel].throttle = initial_right

def backward():
  initial_left = -0.05
  initial_right = -0.05
  kit.continuous_servo[left_channel].throttle = initial_left
  kit.continuous_servo[right_channel].throttle = initial_right

def left():
  initial_left = -0.05
  initial_right = 0.3
  kit.continuous_servo[left_channel].throttle = initial_left
  kit.continuous_servo[right_channel].throttle = initial_right

def right():
  initial_left = 0.3
  initial_right = -0.05
  kit.continuous_servo[left_channel].throttle = initial_left
  kit.continuous_servo[right_channel].throttle = initial_right

def stopX():
  initial_left = 0.1
  initial_right = 0.1
  kit.continuous_servo[left_channel].throttle = initial_left 
  kit.continuous_servo[right_channel].throttle = initial_right

def ascend():
  initial_left_v = 0.3
  initial_right_v = 0.3
  kit.continuous_servo[left_v_channel].throttle = initial_left_v 
  kit.continuous_servo[right_v_channel].throttle = initial_right_v

def descend():
  initial_left_v = -0.05
  initial_right_v = -0.05
  kit.continuous_servo[left_v_channel].throttle = initial_left_v 
  kit.continuous_servo[right_v_channel].throttle = initial_right_v

def stopY():
  initial_left_v = 0.1
  initial_right_v = 0.1
  kit.continuous_servo[left_v_channel].throttle = initial_left_v 
  kit.continuous_servo[right_v_channel].throttle = initial_right_v

time.sleep(5)
forward()
time.sleep(10)
stopX()
time.sleep(2)
backward()
time.sleep(5)
stopX()
time.sleep(2)


