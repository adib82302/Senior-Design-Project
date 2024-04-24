import serial
import time

buffer_RTT = [0]*4
COM = 0x55
Distance = 0

ser = serial.Serial('/dev/ttyAMA1', 115200)

def calculatechecksum(data):
	return(sum(data)&0xFF)
	
def read_sensor():
	ser.write(bytes([COM]))
	time.sleep(0.1)
	
	if ser.inWaiting() > 0:
		if ser.read(1)[0] == 0xFF:
			buffer_RTT[0] = 0xFF
			for i in range(1,4):
				buffer_RTT[i] = ord(ser.read(1))
			
			CS = buffer_RTT[0] +buffer_RTT[1] + buffer_RTT[2]
		
			if buffer_RTT[3] == CS & 0xFF:
				Distance = (buffer_RTT[1] << 8) + buffer_RTT[2]
				print(Distance)
				
				
if __name__ == '__main__':
	try:
		#ser.open()
		print("Serial port open")
		
		while True:
			read_sensor()
			time.sleep(0.1)
	except KeyboardInterrupt:
		print("exiting")
	finally:
		ser.close()
