#!/usr/bin/env python3

import datetime
import huelevels
import hues
import logging
import pytz
import time
from astral import Astral
from phue import Bridge

logging.basicConfig(level=logging.INFO)

localtz = pytz.timezone ("America/New_York")

schedule = hues.Schedule()
schedule.setTimeZone("America/New_York")
astral = Astral()
astral.solar_depression = 'civil'
city = astral["Orlando"]
sun = city.sun(date = datetime.date.today(), local = True)
sunriseTime = sun["sunrise"] + datetime.timedelta(days = 1)
sunriseLightsOffTime = sunriseTime + datetime.timedelta(minutes = 30)
sunsetLightsOnTime = sun["sunset"] - datetime.timedelta(minutes = 60)

allLights = ["FamilyRoomTorch", "FamilyRoomLeft", "FamilyRoomRight", "MasterBedroomHis", "MasterBedroomHers"]
familyRoom = ["FamilyRoomTorch", "FamilyRoomLeft", "FamilyRoomRight"]
masterBedroom = ["MasterBedroomHis", "MasterBedroomHers"]

def transitionRelaxToEnergize(beginDateTime, endDateTime, lightNames):
	deltaDateTime = endDateTime - beginDateTime
	deltaDateTimeInSeconds = deltaDateTime / datetime.timedelta(seconds = 1)

	secondsPerTransition = int(deltaDateTimeInSeconds / 3)
	durationBetweenEventsInDeciseconds = secondsPerTransition * 10
	transitionTimeInDeciseconds = (secondsPerTransition - 1) * 10
	logging.info("deltaTime: " + str(deltaDateTime))
	logging.info("minutesPerTransition: " + str(secondsPerTransition / 60))

	if (deltaDateTimeInSeconds > 0):
		schedule.addGroupEvent(beginDateTime, lightNames, 'reading', transitionTimeInDeciseconds)
		schedule.addGroupEventByOffsetToLast(durationBetweenEventsInDeciseconds, lightNames, 'white', transitionTimeInDeciseconds)
		schedule.addGroupEventByOffsetToLast(durationBetweenEventsInDeciseconds, lightNames, 'energize', transitionTimeInDeciseconds)
	else:
		schedule.addGroupEvent(endDateTime - datetime.timedelta(minutes = 1), 0, lightNames, 'energize', 0)

def transitionEnergizeToRelax(beginDateTime, endDateTime, lightNames):
	deltaDateTime = endDateTime - beginDateTime
	deltaDateTimeInSeconds = deltaDateTime / datetime.timedelta(seconds = 1)

	secondsPerTransition = int(deltaDateTimeInSeconds / 3)
	durationBetweenEventsInDeciseconds = secondsPerTransition * 10
	transitionTimeInDeciseconds = (secondsPerTransition - 1) * 10
	logging.info("deltaTime: " + str(deltaDateTime))
	logging.info("minutesPerTransition: " + str(secondsPerTransition / 60))

	schedule.addGroupEvent(beginDateTime, lightNames, 'white', 30 * 10)
	schedule.addGroupEventByOffsetToLast(durationBetweenEventsInDeciseconds, lightNames, 'reading', transitionTimeInDeciseconds)
	schedule.addGroupEventByOffsetToLast(durationBetweenEventsInDeciseconds, lightNames, 'relax', transitionTimeInDeciseconds)

def morningRoutine(beginDateTime, lightNames):
	currentTime = beginDateTime

	if (currentTime < sunriseLightsOffTime):
		schedule.addGroupEvent(currentTime, lightNames, 'orangeLow', 0, lightOn = True)

	currentTime += datetime.timedelta(minutes = 15)

	if (currentTime < sunriseLightsOffTime):
		schedule.addGroupEvent(currentTime, lightNames, 'yellowSun', 9 * 60 * 10)

	currentTime += datetime.timedelta(minutes = 10)

	if (currentTime < sunriseLightsOffTime):
		schedule.addGroupEvent(currentTime, lightNames, 'relax', 4 * 60 * 10)

	currentTime += datetime.timedelta(minutes = 5)
	transitionRelaxToEnergize(currentTime, sunriseTime, lightNames)

def bedTimeRoutine(beginDateTime, lightNames):
	currentTime = beginDateTime

	schedule.addGroupEvent(currentTime, lightNames, 'yellowSun', 29 * 60 * 10)
	schedule.addGroupEventByOffsetToLast(30 * 60 * 10, lightNames, 'orangeLow', 15 * 60 * 10)
	schedule.addGroupEventByOffsetToLast(30 * 60 * 10, lightNames, 'orangeLow', 0, lightOn = False)

def setupSchedule(bedTimeHis, bedTimeHers, sleepDurationHis, sleepDurationHers):
	bridge = Bridge('huebridge', 'newdeveloper')
	# bridge.connect()
	#bridge.get_api()

	# lightsByName = bridge.get_light_objects('name')
	# for light in lightsByName:
	# 	print(str(light))

	schedules = bridge.get_schedule()
	logging.info("Removing old schedules")
	for i in schedules:
		bridge.delete_schedule(i)

	logging.info(sunsetLightsOnTime.strftime("%H:%M:%S turn on lights"))
	schedule.addGroupEvent(sunsetLightsOnTime, allLights, 'energize', 30 * 60 * 10, lightOn = True)

	logging.info("sunset is at " + str(sun["sunset"]))
	transitionEnergizeToRelax(sun["sunset"], bedTimeHers - datetime.timedelta(hours = 1), allLights)

	bedTimeStartTimeMasterBedroom = bedTimeHers - datetime.timedelta(minutes = 30)
	bedTimeStartTimeFamilyRoom = bedTimeHis - datetime.timedelta(minutes = 30)
	if (bedTimeHis != bedTimeHers):
		bedTimeRoutine(bedTimeStartTimeMasterBedroom, masterBedroom)
		bedTimeRoutine(bedTimeStartTimeFamilyRoom, familyRoom)

		turnOnMasterBedroomLightTime = bedTimeHis - datetime.timedelta(minutes = 5)
		turnOffMasterBedroomLightTime = bedTimeHis + datetime.timedelta(minutes = 30)
		schedule.addEvent(turnOnMasterBedroomLightTime, 'MasterBedroomHis', 'orangeLow', 0, lightOn = True)
		schedule.addEvent(turnOffMasterBedroomLightTime, 'MasterBedroomHis', 'orangeLow', 0, lightOn = False)
	else:
		bedTimeRoutine(bedTimeStartTimeFamilyRoom, allLights)

	wakeUpTimeHis = bedTimeHis + datetime.timedelta(hours = sleepDurationHis)
	wakeUpTimeHers = bedTimeHers + datetime.timedelta(hours = sleepDurationHers)
	if (wakeUpTimeHis != wakeUpTimeHers):
		lightsOnHers = wakeUpTimeHers - datetime.timedelta(minutes = 15)
		lightsOffHers = wakeUpTimeHers + datetime.timedelta(minutes = 30)
		schedule.addEvent(lightsOnHers, 'MasterBedroomHers', 'orangeLow', 0, lightOn = True)
		schedule.addEvent(lightsOffHers, 'MasterBedroomHers', 'orangeLow', 0, lightOn = False)

		morningRoutine(lightsOnHers, familyRoom)
		lightsOnHis = wakeUpTimeHis - datetime.timedelta(minutes = 15)
		morningRoutine(lightsOnHis, masterBedroom)
	else:
		lightsOnTime = wakeUpTimeHers - datetime.timedelta(minutes = 15)
		morningRoutine(lightsOnTime, allLights)

	logging.info("sunrise is at " + str(sun["sunrise"]))
	logging.info(sunriseLightsOffTime.strftime("%H:%M:%S turn off lights"))
	schedule.addGroupEvent(sunriseLightsOffTime, allLights, 'energize', 30 * 60 * 10, lightOn = False)


if __name__ == '__main__':
	weekday = datetime.datetime.now().weekday()
	bedTimeHers = schedule.getLocalDateTime(22, 0, 0)
	bedTimeHis = bedTimeHers
	sleepDurationHis = 8
	sleepDurationHers = 8
	if (weekday == 4 or weekday == 5):
		bedTimeHis = schedule.getLocalDateTime(23, 0, 0)
	elif (weekday == 0):
		bedTimeHis = schedule.getLocalDateTime(0, 0, 0)
		bedTimeHis += datetime.timedelta(days = 1)
		sleepDurationHis = 7

	setupSchedule(bedTimeHis, bedTimeHers, sleepDurationHis, sleepDurationHers)
