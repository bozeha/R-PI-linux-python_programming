import datetime
import RPi.GPIO as GPIO
import json
import threading
import time
now = datetime.datetime.now()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
mainLoop = True
arrayOfElements = []
def init():
	print ("start init")
	data = LoadFromJson()

	lightScheduleControlStatus = data["light"]["schedule_control"]["status"]
	lightScheduleControlTurnOffAtHour = data["light"]["schedule_control"]["turn_off_at"]["hour"]
	lightScheduleControlTurnOffAtMinutes = data["light"]["schedule_control"]["turn_off_at"]["minutes"]
	lightScheduleControlTurnOnAtHour = data["light"]["schedule_control"]["turn_on_at"]["hour"]
	lightScheduleControlTurnOnAtMinutes = data["light"]["schedule_control"]["turn_on_at"]["minutes"]

	waterPumpIntervalControlStatus = data["water_pump"]["interval_control"]["status"]
	waterPumpIntervalRunTimeHour = data["water_pump"]["interval_control"]["run_time"]["hour"]
	waterPumpIntervalRunTimeMinutes = data["water_pump"]["interval_control"]["run_time"]["minutes"]
	waterPumpIntervalDuration = data["water_pump"]["interval_control"]["duration_in_sec"]


	light = ScheduleElement("Light",6,"OUT",'', lightScheduleControlStatus, lightScheduleControlTurnOffAtHour, lightScheduleControlTurnOffAtMinutes, lightScheduleControlTurnOnAtHour, lightScheduleControlTurnOnAtMinutes)

	waterPump = IntervalElement("WaterPump",20,"OUT",'', waterPumpIntervalControlStatus, waterPumpIntervalRunTimeHour, waterPumpIntervalRunTimeMinutes, waterPumpIntervalDuration)

	arrayOfElements.append(light)
	arrayOfElements.append(waterPump)

	waterPump.TurnOff()
#	light.TurnOff()

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
	def __init__(self, name, port, state, value, lightScheduleControlStatus, lightScheduleControlTurnOnAtHour, lightScheduleControlTurnOnAtMinutes, lightScheduleControlTurnOffAtHour, lightScheduleControlTurnOffAtMinutes):
		super().__init__(name, port, state, value)
		self.setScheduleStatus(lightScheduleControlStatus)
		self.setStartTime(lightScheduleControlTurnOnAtHour, lightScheduleControlTurnOnAtMinutes)
		self.setEndTime(lightScheduleControlTurnOffAtHour, lightScheduleControlTurnOffAtMinutes)

	def setScheduleStatus(self, status):
		self.ScheduleStatus = status

	def setStartTime(self, hour, minutes):
		self.startTimeHour = hour
		self.startTimeMinutes =minutes

	def setEndTime(self, hour, minutes):
		self.endTimeHour = hour
		self.endTimeMinutes = minutes


class IntervalElement(Element):
	def __init__(self, name, port, state, value, waterPumpIntervalControlStatus, waterPumpIntervalRunTimeHour, waterPumpIntervalRunTimeMinutes, waterPumpIntervalDuration):
		super().__init__(name, port, state, value)

		self.setIntervalStatus(waterPumpIntervalControlStatus)
		self.setRunTime(waterPumpIntervalRunTimeHour, waterPumpIntervalRunTimeMinutes)
		self.setDurationInSec(waterPumpIntervalDuration)

	def setIntervalStatus(self, status):
		self.intervalStatus = status

	def setRunTime(self, hour, minutes):
		self.runTimeHour = hour
		self.runTimeMinutes = minutes

	def setDurationInSec(self, duration):
		self.durationInSec = duration


def main ():
	while mainLoop == True:
		for element in arrayOfElements:
			if(isinstance(element, IntervalElement)):
				if(element.intervalStatus == "true"):
					if(element.runTimeHour == Time.hour and element.runTimeMinutes == Time.minutes):
						element.setIntervalStatus = "false"
						element.runTimeOut(self.durationInSec)
			elif(isinstance(element, ScheduleElement)):
				print(" ")

init()
main()
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

