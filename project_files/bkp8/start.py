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
	lightScheduleHasBeenActivated = data["light"]["schedule_control"]["been_activated"]
	lightScheduleControlTurnOffAtHour = data["light"]["schedule_control"]["turn_off_at"]["hour"]
	lightScheduleControlTurnOffAtMinutes = data["light"]["schedule_control"]["turn_off_at"]["minutes"]
	lightScheduleControlTurnOnAtHour = data["light"]["schedule_control"]["turn_on_at"]["hour"]
	lightScheduleControlTurnOnAtMinutes = data["light"]["schedule_control"]["turn_on_at"]["minutes"]

	waterPumpIntervalControlStatus = data["water_pump"]["interval_control"]["status"]
	waterPumpIntervalHasBeenActivated = data["water_pump"]["interval_control"]["been_activated"]
	waterPumpIntervalRunTimeHour = data["water_pump"]["interval_control"]["run_time"]["hour"]
	waterPumpIntervalRunTimeMinutes = data["water_pump"]["interval_control"]["run_time"]["minutes"]
	waterPumpIntervalDuration = data["water_pump"]["interval_control"]["duration_in_sec"]

	light = ScheduleElement("Light",6,"OUT",'', lightScheduleControlStatus, lightScheduleControlTurnOnAtHour, lightScheduleControlTurnOnAtMinutes, lightScheduleControlTurnOffAtHour, lightScheduleControlTurnOffAtMinutes, lightScheduleHasBeenActivated)

	waterPump = IntervalElement("WaterPump",20,"OUT",'', waterPumpIntervalControlStatus, waterPumpIntervalRunTimeHour, waterPumpIntervalRunTimeMinutes, waterPumpIntervalDuration, waterPumpIntervalHasBeenActivated)

	arrayOfElements.append(light)
	arrayOfElements.append(waterPump)

	waterPump.turnOn()
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
	def changeState(self, state):
		if state == "OUT":
			GPIO.setup(self.port, GPIO.OUT)
		elif state == "IN":
			GPIO.setup(self.port, GPIO.IN)
	def turnOn(self):
		print("turn on "+self.name)
		self.changeState(self.state)
		GPIO.output(self.port, GPIO.HIGH)
	def turnOff(self):
		print("turn off "+self.name)
		self.changeState(self.state)
		GPIO.output(self.port, GPIO.LOW)
	def runWithTimeOut(self, seconds):
		print("turn on element: "+self.name+" in port "+str(self.port) +" for enterval of: "+str(seconds)+" seconds")
		self.turnOn()
		time.sleep(int(seconds))
		self.turnOff()
class Time:
	def __init__(self):
		self.update()
	def update(self):
		current = datetime.datetime.now()
		self.year = current.year
		self.month = current.month
		self.day = current.day
		self.hour = current.hour
		self.minute = current.minute
		self.second = current.second
		self.microsecond = current.microsecond
	def getYear(self):
		return self.year
	def getMonth(self):
		return self.month
	def getDay(self):
		return self.day
	def getHour(self):
		if(self.hour < 10):
			return "0"+str(self.hour)
		else:
			return self.hour
	def getMinutes(self):
		if(self.minute < 10):
			return "0"+str(self.minute)
		else:
			return self.minute
	def getSecond(self):
		return self.second
	def getMicroSec(self):
		return self.microsecond


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
	def __init__(self, name, port, state, value, scheduleControlStatus, scheduleControlTurnOnAtHour, scheduleControlTurnOnAtMinutes, scheduleControlTurnOffAtHour, scheduleControlTurnOffAtMinutes, scheduleHasBeenActivated):
		super().__init__(name, port, state, value)
		self.setScheduleStatus(scheduleControlStatus)
		self.setStartTime(scheduleControlTurnOnAtHour, scheduleControlTurnOnAtMinutes)
		self.setEndTime(scheduleControlTurnOffAtHour, scheduleControlTurnOffAtMinutes)
		self.setScheduleHasBeenActivated(scheduleHasBeenActivated)

	def setScheduleStatus(self, status):
		self.scheduleStatus = status

	def setStartTime(self, hour, minutes):
		self.startTimeHour = hour
		self.startTimeMinutes =minutes

	def setEndTime(self, hour, minutes):
		self.endTimeHour = hour
		self.endTimeMinutes = minutes

	def setScheduleHasBeenActivated(self, active):
		self.scheduleBeenActivated = bool(active)

	def scheduleActivated(self):
		self.scheduleBeenActivated = True

	def scheduleDesactivated(self):
		self.scheduleBeenActivated = False

class IntervalElement(Element):
	def __init__(self, name, port, state, value, intervalControlStatus, intervalRunTimeHour, intervalRunTimeMinutes, intervalDuration, intervalHasBeenActivated):
		super().__init__(name, port, state, value)

		self.setIntervalStatus(intervalControlStatus)
		self.setRunTime(intervalRunTimeHour, intervalRunTimeMinutes)
		self.setDurationInSec(intervalDuration)
		self.setIntervalHasBeenActivated(intervalHasBeenActivated)

	def setIntervalStatus(self, status):
		self.intervalStatus = status

	def setRunTime(self, hour, minutes):
		self.runTimeHour = hour
		self.runTimeMinutes = minutes

	def setDurationInSec(self, duration):
		self.durationInSec = duration

	def setIntervalHasBeenActivated(self, active):
		self.intervalBeenActivated = bool(active)

	def intervalActivated(self):
		self.intervalBeenActivated = True

	def intervalDesactivated(self):
		self.intervalBeenActivated = False

def main ():
	currentTime = Time()
	print("enter main function")
	while mainLoop == True:
#		print("main loop")
		for element in arrayOfElements:
			if(isinstance(element, IntervalElement)):

				if(element.intervalStatus == "true" and element.intervalBeenActivated == False):
#					print(element.runTimeHour+ "::" + str(currentTime.getHour()) + "::" + element.runTimeMinutes + "::" + str(currentTime.getMinutes()))
					if(element.runTimeHour == str(currentTime.getHour()) and element.runTimeMinutes == str(currentTime.getMinutes())):
						print(element.name +" interval status run !!!")

################################################  prevent loop interval , will get right value on init ->update from json
						element.intervalActivated()

################################################ run interval as thread
						threadForInterval = threading.Thread(target = element.runWithTimeOut, args = (element.durationInSec, ))
						threadForInterval.start()

			elif(isinstance(element, ScheduleElement)):
				if(element.scheduleStatus == "true" and element.scheduleBeenActivated == False):
					if(element.endTimeHour == str(currentTime.getHour()) and element.endTimeMinutes >= str(currentTime.getMinutes())) or \
					(element.startTimeHour == str(currentTime.getHour()) and element.startTimeMinutes <= str(currentTime.getMinutes()) and (element.endTimeMinutes > str(currentTime.getMinutes()) or element.endTimeHour > str(currentTime.getHour()))) or \
					(element.startTimeHour < str(currentTime.getHour()) and element.endTimeHour > str(currentTime.getHour())):
						element.turnOn()

						element.scheduleActivated()

				elif(element.scheduleStatus == "true" and element.scheduleBeenActivated == True):
					if(element.scheduleStatus == "false"):
						

############### update current time every loop
		currentTime.update()


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

