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
sunriseLightsOffTime = sun["sunrise"] + datetime.timedelta(minutes = 30)
sunsetLightsOnTime = sun["sunset"] - datetime.timedelta(minutes = 60)

allLights = ["FamilyRoomTorch", "FamilyRoomLeft", "FamilyRoomRight", "MasterBedroomHis", "MasterBedroomHers"]
familyRoom = ["FamilyRoomTorch", "FamilyRoomLeft", "FamilyRoomRight"]
masterBedroom = ["MasterBedroomHis", "MasterBedroomHers"]

def transitionRelaxToEnergize(beginHour, beginMinute, endHour, endMinute, lightNames):
	endInMinutes = (endHour * 60) + endMinute
	beginInMinutes = (beginHour * 60) + beginMinute

	deltaTime = endInMinutes - beginInMinutes
	minutesPerTransition = int(deltaTime / 3)
	durationBetweenEventsInDeciseconds = minutesPerTransition * 60 * 10
	transitionTimeInDeciseconds = (minutesPerTransition - 1) * 60 * 10
	logging.info("deltaTime: " + str(deltaTime))
	logging.info("minutesPerTransition: " + str(minutesPerTransition))

	if (deltaTime > 2):
		schedule.addGroupEvent(beginHour, beginMinute, 0, lightNames, 'reading', transitionTimeInDeciseconds)
		schedule.addGroupEventByOffsetToLast(durationBetweenEventsInDeciseconds, lightNames, 'white', transitionTimeInDeciseconds)
		schedule.addGroupEventByOffsetToLast(durationBetweenEventsInDeciseconds, lightNames, 'energize', transitionTimeInDeciseconds)
	else:
		schedule.addGroupEvent(endHour, endMinute - 1, 0, lightNames, 'energize', 0)

def transitionEnergizeToRelax(beginHour, beginMinute, endHour, endMinute, lightNames):
	endInMinutes = (endHour * 60) + endMinute
	beginInMinutes = (beginHour * 60) + beginMinute

	deltaTime = endInMinutes - beginInMinutes
	minutesPerTransition = int(deltaTime / 4)
	durationBetweenEventsInDeciseconds = minutesPerTransition * 60 * 10
	transitionTimeInDeciseconds = (minutesPerTransition - 1) * 60 * 10
	logging.info("deltaTime: " + str(deltaTime))
	logging.info("minutesPerTransition: " + str(minutesPerTransition))

	schedule.addGroupEvent(beginHour, beginMinute, 0, lightNames, 'white', 30 * 10)
	schedule.addGroupEventByOffsetToLast(durationBetweenEventsInDeciseconds, lightNames, 'reading', transitionTimeInDeciseconds)
	schedule.addGroupEventByOffsetToLast(durationBetweenEventsInDeciseconds, lightNames, 'relax', transitionTimeInDeciseconds)

def morningRoutine(beginHour, beginMinute, lightNames):
	currentTime = datetime.datetime.now()
	currentTime = currentTime.replace(hour = beginHour, minute = beginMinute, second = 0)
	currentTime = localtz.localize(currentTime)#, is_dst=None)

	if (currentTime < sunriseLightsOffTime):
		schedule.addGroupEvent(currentTime.hour, currentTime.minute, currentTime.second, lightNames, 'orangeLow', 0)

	currentTime += datetime.timedelta(minutes = 15)

	if (currentTime < sunriseLightsOffTime):
		schedule.addGroupEvent(currentTime.hour, currentTime.minute, currentTime.second, lightNames, 'yellowSun', 9 * 60 * 10)

	currentTime += datetime.timedelta(minutes = 10)

	if (currentTime < sunriseLightsOffTime):
		schedule.addGroupEvent(currentTime.hour, currentTime.minute, currentTime.second, lightNames, 'relax', 4 * 60 * 10)

	currentTime += datetime.timedelta(minutes = 5)
	transitionRelaxToEnergize(currentTime.hour, currentTime.minute, sun["sunrise"].hour, sun["sunrise"].minute, lightNames)

def bedTimeRoutine(beginHour, beginMinute, lightNames):
	currentTime = datetime.datetime.now()
	currentTime = currentTime.replace(hour = beginHour, minute = beginMinute, second = 0)

	schedule.addGroupEvent(currentTime.hour, currentTime.minute, currentTime.second, lightNames, 'yellowSun', 29 * 60 * 10)
	schedule.addGroupEventByOffsetToLast(30 * 60 * 10, lightNames, 'orangeLow', 15 * 60 * 10)
	schedule.addGroupEventByOffsetToLast(30 * 60 * 10, lightNames, 'orangeLow', 0, lightOn = False)

def setupSchedule(bedTimeHisHour, bedTimeHisMinute, bedTimeHersHour, bedTimeHersMinute, sleepDuration):
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
	schedule.addGroupEvent(sunsetLightsOnTime.hour, sunsetLightsOnTime.minute, sunriseLightsOffTime.second, allLights, 'energize', 30 * 60 * 10, lightOn = True)

	logging.info("sunset is at " + str(sun["sunset"]))
	transitionEnergizeToRelax(sun["sunset"].hour, sun["sunset"].minute, 21, 0, allLights)

	bedTimeHis = schedule.getLocalDateTime(bedTimeHisHour, bedTimeHisMinute, 0)
	bedTimeHers = schedule.getLocalDateTime(bedTimeHersHour, bedTimeHersMinute, 0)
	bedTimeStartTimeMasterBedroom = bedTimeHers - datetime.timedelta(minutes = 30)
	bedTimeStartTimeFamilyRoom = bedTimeHis - datetime.timedelta(minutes = 30)
	if (bedTimeHisHour != bedTimeHersHour or bedTimeHisMinute != bedTimeHersMinute):
		bedTimeRoutine(bedTimeStartTimeMasterBedroom.hour, bedTimeStartTimeMasterBedroom.minute, masterBedroom)
		bedTimeRoutine(bedTimeStartTimeFamilyRoom.hour, bedTimeStartTimeFamilyRoom.minute, familyRoom)

		turnOffMasterBedroomLightTime = bedTimeHis + datetime.timedelta(minutes = 30)
		schedule.addEvent(bedTimeHis.hour, bedTimeHisMinute, 0, 'MasterBedroomHis', 'orangeLow', 0, lightOn = True)
		schedule.addEvent(turnOffMasterBedroomLightTime.hour, turnOffMasterBedroomLightTime.minute, 0, 'MasterBedroomHis', 'orangeLow', 0, lightOn = False)
	else:
		bedTimeRoutine(bedTimeStartTimeFamilyRoom.hour, bedTimeStartTimeFamilyRoom.minute, allLights)

	wakeUpTimeHis = bedTimeHis + datetime.timedelta(hours = sleepDuration)
	wakeUpTimeHers = schedule.getLocalDateTime(6, 0, 0)
	if (wakeUpTimeHis != wakeUpTimeHers):
		lightsOnHers = wakeUpTimeHers - datetime.timedelta(minutes = 15)
		lightsOffHers = wakeUpTimeHers + datetime.timedelta(minutes = 15)
		schedule.addEvent(lightsOnHers.hour, lightsOnHers.minute, 0, 'MasterBedroomHers', 'orangeLow', 0, lightOn = True)
		schedule.addGroupEvent(lightsOffHers.hour, lightsOffHers.minute, 0, 'MasterBedroomHers', 'orangeLow', 0, lightOn = False)

		morningRoutine(lightsOnHers.hour, lightsOnHers.minute, familyRoom)
		lightsOnHis = wakeUpTimeHis - datetime.timedelta(minutes = 15)
		morningRoutine(lightsOnHis.hour, lightsOnHis.minute, masterBedroom)
	else:
		lightsOnTime = wakeUpTimeHers - datetime.timedelta(minutes = 15)
		morningRoutine(lightsOnTime.hour, lightsOnTime.minute, allLights)

	logging.info("sunrise is at " + str(sun["sunrise"]))
	logging.info(sunriseLightsOffTime.strftime("%H:%M:%S turn off lights"))
	schedule.addGroupEvent(sunriseLightsOffTime.hour, sunriseLightsOffTime.minute, sunriseLightsOffTime.second, allLights, 'energize', 30 * 60 * 10, lightOn = False)


if __name__ == '__main__':
	weekday = datetime.datetime.now().weekday()
	if (weekday == 4 or weekday == 5):
		setupSchedule(23, 0, 22, 0, 8)
	else:
		setupSchedule(22, 0, 22, 0, 8)
