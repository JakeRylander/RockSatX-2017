import serial
import time
import RPi.GPIO as GPIO

#Serial Setup

serialOUT = serial.Serial(port = '/dev/ttyAMA0', baudrate = 19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

#Board Pin Mode Setup

GPIO.setmode(GPIO.BCM)

#Variable Definitions
#Components

Proximity_Sensor = 5

#Flags
Launch = 22
Skirt = 23
PowerOffin30 = 24

#IO Setup
#Flags
GPIO.setup(Launch, GPIO.IN)
GPIO.setup(Skirt, GPIO.IN)
GPIO.setup(PowerOffin30, GPIO.IN)

#Proximity Sensor
GPIO.setup(Proximity_Sensor, GPIO.IN)
	
#--------------------------------------------------------------------------
#Begin Program
#Starting Print

serialOUT.write('This software is for IO Testing. \n'.encode())


while(true):
	serialOUT.write('Current Values are: Launch Signal= '.encode())
	serialOUT.write(str(GPIO.input(Launch)).encode())
	serialOUT.write(' |Skirt Signal= '.encode())
	serialOUT.write(str(GPIO.input(Skirt)).encode())
	serialOUT.write(' |PowerOffin30 Signal= '.encode())
	serialOUT.write(str(GPIO.input(PowerOffin30)).encode())
	serialOUT.write(' |ProximitySensor Signal= '.encode())
	serialOUT.write(str(GPIO.input(Proximity_Sensor)).encode())
	serialOUT.write('\n'.encode())
	time.sleep(.10)