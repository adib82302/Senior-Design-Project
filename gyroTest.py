import adafruit_bno055
import board
import time

i2c = board.I2C()

sensor = adafruit_bno055.BNO055_I2C(i2c)
x = True

while x:
	print(sensor.acceleration)
	print(sensor.gyro)
	time.sleep(.5)
