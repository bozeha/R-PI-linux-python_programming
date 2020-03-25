import datetime
import RPi.GPIO as GPIO
import json
import threading
import time
now = datetime.datetime.now()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


def init():
	print ("start init")
	data = LoadFromJson()
	light = ScheduleElement("Light",6,"OUT","", data)
	waterPump = ScheduleElement("WaterPump",20,"OUT","", data)
#  for (k, v) in data.items():
#               print("key: " +k)
#               print("value: " + str(v))
#	data = LoadFromJson()
#	print (data["light"]["normal_control"]["status"])
	#TimeControler(data)


class Element:
	def __init__(self, name, port, state, value):
		self.name = name
		self.port = port
		self.state = state
		self.value = value
		print("new element: "+self.name)
	def ChangeState(self, state):
		if state == "OUT":
			GPIO.setup(self.port, GPIO.OUT)
		elif state == "IN":
			GPIO.setup(self.port, GPIO.IN)
	def TurnOn(self):
		print("turn on "+self.name)
		self.ChangeState(self.state)
		GPIO.output(self.port, GPIO.HIGH)
	def TurnOff(self):
		print("turn off "+self.name)
		self.ChangeState(self.state)
		GPIO.output(self.port, GPIO.LOW)
	def RunWithTimeOut(self, seconds):
		self.TurnOn()
		time.sleep(seconds)
		self.TurnOff()
class Time:
	def __init__(self):
		self.current = datetime.datetime.now()
		self.year = self.current.year
		self.month = self.current.month
		self.day = self.current.day
		self.hour = self.current.hour
		self.minute = self.current.minute
		self.second = self.current.second
		self.microsecond = self.current.microsecond

class SoilMoisture:
	def __init__(self, name, pin):
		self.pin = pin
		self.name = name
		GPIO.setup(pin, GPIO.IN)
	def start(self):
		if(GPIO.input(21) == 0):
			print ("on")
		else:
			print ("off")



def LoadFromJson():
	with open("preferences.json") as f:
		data = json.load(f)
		print("loads json")
		return data


class ScheduleElement(Element):
	def __init__(self, name, port, state, value, data):
	  super().__init__(name, port, state, value)

	def start():
		print("")




init()
#LoadFromJson()
#light = Element("Light",6,"OUT","")
#waterPump = Element("WaterPump",20,"OUT","")

#light = Element("Light",6,"OUT","")
#waterPump = Element("WaterPump",20,"OUT","")

#light.TurnOn()
#timeObj = Time()
#print (timeObj.year)
#time.sleep(3)
#threadForWaterPump = threading.Thread(target=waterPump.RunWithTimeOut, args=(10, ))
#threadForWaterPump.start()
#light.TurnOff()
#time.sleep(3)



#soil = SoilMoisture("soilMoisture",21)

#while True:
#	soil.start()
#	time.sleep(1)
#	print (timeObj.hour)
#	print (timeObj.minute)

