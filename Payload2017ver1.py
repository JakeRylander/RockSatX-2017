import serial
import time
import RPi.GPIO as GPIO
from Stepper import Stepper
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

#Serial Setup

serialOUT = serial.Serial(port = '/dev/ttyAMA0', baudrate = 19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

#Board Pin Mode Setup

GPIO.setmode(GPIO.BCM)

#Variable Definitions
#Components
Inhibit = 19
Leica = 20
Proximity_Sensor = 5
Plasma = 18
UV = 4

#Stepper Motor
Step_Ena = 12
Step_Dir = 13
Step_Step = 16

#Flags
Launch = 22
Skirt = 23
PowerOffin30 = 24

#Misc
time_to_launch = 20 #240 for full sequence

#IO Setup
#Inhibit
GPIO.setup(Inhibit, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#CameraLeica 
GPIO.setup(Leica, GPIO.OUT)

#Stepper Motor
GPIO.setup(Step_Ena, GPIO.OUT)
GPIO.setup(Step_Dir, GPIO.OUT)
GPIO.setup(Step_Step, GPIO.OUT)

#Flags
GPIO.setup(Launch, GPIO.IN)
GPIO.setup(Skirt, GPIO.IN)
GPIO.setup(PowerOffin30, GPIO.IN)

#Proximity Sensor
GPIO.setup(Proximity_Sensor, GPIO.IN)

#Plasma
GPIO.setup(Plasma, GPIO.OUT)

#UV
GPIO.setup(UV, GPIO.OUT)

#Stepper Setup

DoorStepper = Stepper([Step_Ena,Step_Dir,Step_Step])

#Clamp Shell Setup

MH = Adafruit_MotorHAT(addr=0x60)
ClampShell = MH.getMotor(1)

#Function Definitions
#Get Time
def GetTime():
	current_time = time.clock() - time_to_launch
	serialOUT.write(str(current_time).encode())
	serialOUT.write('\n'.encode())
	
#Turn on Leica
def TurnOnLeica():
	GPIO.output(Leica, GPIO.HIGH)
	time.sleep(1)
	GPIO.output(Leica, GPIO.LOW)
	
#Open Door
def OpenDoor():
	
	#Open ClampShell
	ClampShell.run(Adafruit_MotorHAT.FORWARD)
	ClampShell.setSpeed(255)
	time.sleep(4)
	ClampShell.setSpeed(0)
	ClampShell.run(Adafruit_MotorHAT.RELEASE)
	#Open Door
	DoorStepper.step(120000, dir = 'right') #Right == Open
	
#Close Door
def CloseDoor():

	#Close Door
	DoorStepper.step(120000, dir = 'left') #Left == Close
	
	#Close Clamp Shell
	ClampShell.run(Adafruit_MotorHAT.BACKWARD)
	ClampShell.setSpeed(255)
	time.sleep(4)
	ClampShell.setSpeed(0)
	ClampShell.run(Adafruit_MotorHAT.RELEASE)
	
#--------------------------------------------------------------------------
#Begin Program
#Starting Print

serialOUT.write('UPR Payload Alive T(sec)= '.encode())
GetTime()
serialOUT.write('Software RockSat X 2017 Revision 6/14/17 \n'.encode())
serialOUT.write('This software is for August Flight \n'.encode())

#Inhibit

while (GPIO.input(Inhibit) == GPIO.LOW):
	serialOUT.write('Payload Inhibited at T(sec)= '.encode())
	GetTime()
	print('payload inhibited')

#Activate UV

GPIO.output(UV, GPIO.HIGH)
	
#Cameras turn on 15 seconds before launch

fifteen_to_launch = time.clock() + (time_to_launch - 15)

while (time.clock() < fifteen_to_launch):
	serialOUT.write('Time to Launch T(sec)= '.encode())
	GetTime()

TurnOnLeica()

serialOUT.write('Leica Camera on T(sec)= '.encode())
GetTime()

while (GPIO.input(Launch) == GPIO.LOW):
	serialOUT.write('Time to Launch T(sec)= '.encode())
	GetTime()

#Rocket Launched
	
serialOUT.write('Launch T(sec)= '.encode())
GetTime()

while (GPIO.input(Skirt) == 0):
	serialOUT.write('Flying Time T(sec)= '.encode())
	GetTime()

#Skirt Off
	
serialOut.write('Skirt Off T(sec)= '.encode())
GetTime()

#Activate Plasma

GPIO.output(Plasma, GPIO.HIGH)

while (time.perf_counter() < (200 + time_to_launch)):
	serialOUT.write('Plasma is ON at T(sec)= '.encode())
	GetTime()

#while (GPIO.input(Proximity_Sensor) == 1):
	#serialOUT.write('Skirt is not clear at T(sec)= '.encode())
	#GetTime()

#Deactivate Plasma and UV
	
GPIO.output(UV, GPIO.LOW)
GPIO.output(Plasma, GPIO.LOW)

serialOUT.write('Plasma and UV are off at T(sec)= '.encode())
GetTime()

#Door Open

serialOUT.write('Door Opening at Started at T(sec)= '.encode())
GetTime()

#Door Opening

OpenDoor()

serialOUT.write('Door Opened at T(sec)= '.encode())
GetTime()

#30 Seconds before Power Off

while(GPIO.input(PowerOffin30) == 1):
	serialOUT.write('Door still open at T(sec)= '.encode())
	GetTime()

#Door Closing
	
serialOUT.write('Door Closing T(sec)= '.encode())
GetTime()

CloseDoor()

#Door Closed

serialOUT.write('Door Closed at T(sec)= '.encode())
GetTime()

#Sequence End

serialOUT.write('Going back Home T(sec)= '.encode())
GetTime()

