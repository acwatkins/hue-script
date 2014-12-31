#!/usr/bin/env python3

import datetime
import huelevels
import pytz
import time
from astral import Astral
from phue import Bridge

localtz = pytz.timezone ("America/New_York")

astral = Astral()
astral.solar_depression = 'civil'
city = astral["Orlando"]
sun = city.sun(date = datetime.date.today(), local = True)
sunriseLightsOffTime = sun["sunrise"] + datetime.timedelta(minutes = 30)
sunsetLightsOnTime = sun["sunset"] - datetime.timedelta(minutes = 60)

familyRoom = ["FamilyRoomTorch", "FamilyRoomLeft", "FamilyRoomRight"]
masterBedroom = ["MasterBedroomHis", "MasterBedroomHers"]

def getUtcTimeString(hour, minute, second):
	currentDateTime = datetime.datetime.now()
	localCurrentDateTime = localtz.localize(currentDateTime)#, is_dst=None)
	localDateTime = localCurrentDateTime
	localDateTime = localDateTime.replace(hour = hour, minute = minute, second = second)
	utcDateTime = localDateTime.astimezone(pytz.utc)
	return utcDateTime.strftime("%Y-%m-%dT%H:%M:%S")

def transitionRelaxToEnergize(beginHour, beginMinute, endHour, endMinute, groupName):
	endInMinutes = (endHour * 60) + endMinute
	beginInMinutes = (beginHour * 60) + beginMinute

	deltaTime = endInMinutes - beginInMinutes
	minutesPerTransition = int(deltaTime / 3)
	print("deltaTime: " + str(deltaTime))
	print("minutesPerTransition: " + str(minutesPerTransition))

	if (deltaTime > 2):
		currentTime = datetime.datetime.now()
		currentTime = currentTime.replace(hour = beginHour, minute = beginMinute, second = 0)

		print(currentTime.strftime("%H:%M - " + groupName + " Fade in to reading"))
		currentConfig = {'on': True, 'ct': huelevels.CT_READING, 'bri': huelevels.BRI_READING, 'transitiontime': (minutesPerTransition - 1) * 60 * 10}
		bridge.create_group_schedule('ReadingMorning', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'TransitionToReading')

		currentTime += datetime.timedelta(minutes = minutesPerTransition)

		print(currentTime.strftime("%H:%M - " + groupName + " Fade in to white light"))
		currentConfig = {'on': True, 'hue': huelevels.HUE_WHITE, 'sat': huelevels.SAT_WHITE, 'bri': huelevels.BRI_ENERGIZE, 'transitiontime': (minutesPerTransition - 1) * 60 * 10}
		bridge.create_group_schedule('WhiteMorning', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'TransitionToWhite')

		currentTime += datetime.timedelta(minutes = minutesPerTransition)

		print(currentTime.strftime("%H:%M - " + groupName + " Fade in to energize"))
		currentConfig = {'on': True, 'ct': huelevels.CT_ENERGIZE, 'bri': huelevels.BRI_ENERGIZE, 'transitiontime': 30 * 10}
		bridge.create_group_schedule('EnergizeMorning', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'TransitionToEnergize')
	else:
		currentTime = sunriseLightsOffTime - datetime.timedelta(minutes = 1)
		print(currentTime.strftime("%H:%M - " + groupName + " Turning lights immediately to energize"))
		currentConfig = {'on': True, 'ct': huelevels.CT_ENERGIZE, 'bri': huelevels.BRI_ENERGIZE, 'transitiontime': (minutesPerTransition - 1) * 60 * 10}
		bridge.create_group_schedule('EnergizeMorning', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'TransitionToEnergize')


def transitionEnergizeToRelax(beginHour, beginMinute, endHour, endMinute, groupName):
	endInMinutes = (endHour * 60) + endMinute
	beginInMinutes = (beginHour * 60) + beginMinute

	deltaTime = endInMinutes - beginInMinutes
	minutesPerTransition = int(deltaTime / 4)
	print("deltaTime: " + str(deltaTime))
	print("minutesPerTransition: " + str(minutesPerTransition))

	currentTime = datetime.datetime.now()
	currentTime = currentTime.replace(hour = beginHour, minute = beginMinute, second = 0)

	print(currentTime.strftime("%H:%M - " + groupName + " Fade out to white light"))
	currentConfig = {'on': True, 'hue': huelevels.HUE_WHITE, 'sat': huelevels.SAT_WHITE, 'bri': huelevels.BRI_ENERGIZE, 'transitiontime': 30 * 10}
	bridge.create_group_schedule('WhiteEvening', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'TransitionToWhite')

	currentTime += datetime.timedelta(minutes = minutesPerTransition)

	print(currentTime.strftime("%H:%M - " + groupName + " Fade out to reading"))
	currentConfig = {'on': True, 'ct': huelevels.CT_READING, 'bri': huelevels.BRI_READING, 'transitiontime': (minutesPerTransition - 1) * 60 * 10}
	bridge.create_group_schedule('ReadingEvening', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'TransitionToReading')

	currentTime += datetime.timedelta(minutes = minutesPerTransition * 2)

	print(currentTime.strftime("%H:%M - " + groupName + " Fade out to relax"))
	currentConfig = {'on': True, 'ct': huelevels.CT_RELAX, 'bri': huelevels.BRI_RELAX, 'transitiontime': (minutesPerTransition - 1) * 60 * 10}
	bridge.create_group_schedule('RelaxEvening', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'TransitionToReading')

def morningRoutine(beginHour, beginMinute, groupName):
	currentTime = datetime.datetime.now()
	currentTime = currentTime.replace(hour = beginHour, minute = beginMinute, second = 0)
	currentTime = localtz.localize(currentTime)#, is_dst=None)

	if (currentTime < sunriseLightsOffTime):
		print(currentTime.strftime("%H:%M - " + groupName + " Turn on lights low red"))
		currentConfig = {'on': True, 'hue': huelevels.HUE_ORANGE_RED, 'sat': huelevels.SAT_ORANGE_RED, 'bri': 1, 'transitiontime': 0}
		bridge.create_group_schedule('OrangeRedOn', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'OnOrangeRed')

	currentTime += datetime.timedelta(minutes = 15)

	if (currentTime < sunriseLightsOffTime):
		print(currentTime.strftime("%H:%M - " + groupName + " Fade in to yellow sun"))
		currentConfig = {'on': True, 'hue': huelevels.HUE_YELLOW_SUN, 'sat': huelevels.SAT_YELLOW_SUN, 'bri': huelevels.BRI_RELAX, 'transitiontime': 9 * 60 * 10}
		bridge.create_group_schedule('YellowSun10Min', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'FadeInYellowSun')

	currentTime += datetime.timedelta(minutes = 10)

	if (currentTime < sunriseLightsOffTime):
		print(currentTime.strftime("%H:%M - " + groupName + " Fade in to relax"))
		currentConfig = {'on': True, 'ct': huelevels.CT_RELAX, 'bri': huelevels.BRI_RELAX, 'transitiontime': 4 * 60 * 10}
		bridge.create_group_schedule('Relax5Min', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'TransitionToRelax')

	currentTime += datetime.timedelta(minutes = 5)
	transitionRelaxToEnergize(currentTime.hour, currentTime.minute, sun["sunrise"].hour, sun["sunrise"].minute, groupName)

def bedTimeRoutine(beginHour, beginMinute, groupName):
	currentTime = datetime.datetime.now()
	currentTime = currentTime.replace(hour = beginHour, minute = beginMinute, second = 0)

	print(currentTime.strftime("%H:%M - " + groupName + " Fade out to yellow sun"))
	currentConfig = {'on': True, 'hue': huelevels.HUE_YELLOW_SUN, 'sat': huelevels.SAT_YELLOW_SUN, 'bri': huelevels.BRI_RELAX, 'transitiontime': 29 * 60 * 10}
	bridge.create_group_schedule('YellowEvening', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'FadeOutYellowSun')

	currentTime += datetime.timedelta(minutes = 30)

	print(currentTime.strftime("%H:%M - " + groupName + " Fade out to low orange red"))
	currentConfig = {'on': True, 'hue': huelevels.HUE_ORANGE_RED, 'sat': huelevels.SAT_ORANGE_RED, 'bri': 0, 'transitiontime': 14 * 60 * 10}
	bridge.create_group_schedule('RedEvening', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'FaidOutOrangeRed')

	currentTime += datetime.timedelta(minutes = 30)

	print(currentTime.strftime("%H:%M - " + groupName + " Turn off lights"))
	currentConfig = {'on': False, 'hue': huelevels.HUE_ORANGE_RED, 'sat': huelevels.SAT_ORANGE_RED, 'bri': 0, 'transitiontime': 0}
	bridge.create_group_schedule('OffEvening', getUtcTimeString(currentTime.hour, currentTime.minute, 0), groupName, currentConfig, 'TurnOffLights')

bridge = Bridge('huebridge', 'newdeveloper')
#bridge.connect()
#bridge.get_api()

# lightsByName = bridge.get_light_objects('name')
# for light in lightsByName:
# 	print(str(light))

schedules = bridge.get_schedule()
print("Removing old schedules")
for schedule in schedules:
	print(str(schedule))
	bridge.delete_schedule(schedule)

weekday = datetime.datetime.now().weekday()
if (weekday == 1 or weekday == 5 or weekday == 6):
	print("05:45 MasterBedroom Turn on lights low red")
	currentConfig = {'on': True, 'hue': huelevels.HUE_ORANGE_RED, 'sat': huelevels.SAT_ORANGE_RED, 'bri': 1, 'transitiontime': 0}
	bridge.create_group_schedule('Wakeup', getUtcTimeString(5, 45, 0), 'MasterBedroom', currentConfig, 'OnOrangeRed')

	print("06:15 MasterBedroom Turn off lights")
	currentConfig = {'on': False, 'hue': huelevels.HUE_ORANGE_RED, 'sat': huelevels.SAT_ORANGE_RED, 'bri': 1, 'transitiontime': 0}
	bridge.create_group_schedule('Wakeup', getUtcTimeString(6, 15, 0), 'MasterBedroom', currentConfig, 'OnOrangeRed')

	morningRoutine(5, 45, "FamilyRoom")
	morningRoutine(6, 45, "MasterBedroom")
else:
	morningRoutine(5, 45, "All")

print("sunrise is at " + str(sun["sunrise"]))
print(sunriseLightsOffTime.strftime("%H:%M:%S turn off lights"))
currentConfig = {'on': False, 'ct': huelevels.CT_ENERGIZE, 'bri': 0, 'transitiontime': 30 * 60 * 10}
bridge.create_group_schedule('Wakeup', getUtcTimeString(sunriseLightsOffTime.hour, sunriseLightsOffTime.minute, 0), 'All', currentConfig, 'TurnOffLights')

print(sunsetLightsOnTime.strftime("%H:%M:%S turn on lights"))
currentConfig = {'on': True, 'ct': huelevels.CT_ENERGIZE, 'bri': huelevels.BRI_ENERGIZE, 'transitiontime': 30 * 60 * 10}
bridge.create_group_schedule('Evening', getUtcTimeString(sunsetLightsOnTime.hour, sunsetLightsOnTime.minute, 0), 'All', currentConfig, 'TurnOffLights')

print("sunset is at " + str(sun["sunset"]))
transitionEnergizeToRelax(sun["sunset"].hour, sun["sunset"].minute, 21, 0, "All")

if (weekday == 4 or weekday == 5):
	bedTimeRoutine(21, 30, "MasterBedroom")
	bedTimeRoutine(22, 30, "FamilyRoom")
else:
	bedTimeRoutine(21, 30, "All")

if (weekday == 0):
	print("23:00 - FamilyRoom, Turning on lights relax")
	currentConfig = {'on': True, 'ct': huelevels.CT_RELAX, 'bri': huelevels.BRI_RELAX, 'transitiontime': 0}
	bridge.create_group_schedule('Wakeup', getUtcTimeString(23, 0, 0), 'FamilyRoom', currentConfig, 'TurnOffLights')	

	print("23:00 - MasterBedroom, Turning on lights low orange-red")
	currentConfig = {'on': True, 'hue': huelevels.HUE_ORANGE_RED, 'sat': huelevels.SAT_ORANGE_RED, 'bri': 1, 'transitiontime': 0}
	bridge.create_schedule('Wakeup', getUtcTimeString(23, 0, 0), 'MasterBedroomHis', currentConfig, 'OnOrangeRed')

	print("23:30 - Turning off lights")
	currentConfig = {'on': False, 'hue': huelevels.HUE_ORANGE_RED, 'sat': huelevels.SAT_ORANGE_RED, 'bri': 1, 'transitiontime': 29 * 60 * 10}
	bridge.create_group_schedule('Wakeup', getUtcTimeString(23, 30, 0), 'All', currentConfig, 'OffOrangeRed')
