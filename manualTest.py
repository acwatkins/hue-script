#!/usr/bin/env python3

import datetime
import huelevels
import pytz
import time
from astral import Astral
from phue import Bridge

import hues

import logging
logging.basicConfig()

localtz = pytz.timezone ("America/New_York")

def getUtcTimeString(hour, minute, second):
	currentDateTime = datetime.datetime.now()
	localCurrentDateTime = localtz.localize(currentDateTime)#, is_dst=None)
	localDateTime = localCurrentDateTime
	localDateTime = localDateTime.replace(hour = hour, minute = minute, second = second)
	utcDateTime = localDateTime.astimezone(pytz.utc)
	return utcDateTime.strftime("%Y-%m-%dT%H:%M:%S")

allLights = ["FamilyRoomTorch", "FamilyRoomLeft", "FamilyRoomRight", "MasterBedroomHis", "MasterBedroomHers"]
familyRoom = ["FamilyRoomTorch", "FamilyRoomLeft", "FamilyRoomRight"]
masterBedroom = ["MasterBedroomHis", "MasterBedroomHers"]

schedule = hues.Schedule()
schedule.setTimeZone("America/New_York")
turnOnTime = datetime.datetime.now()
turnOnTime = schedule.localtz.localize(turnOnTime)
print(turnOnTime.strftime("%H:%M:%S"))
turnOnTime += datetime.timedelta(seconds = 2)
print(turnOnTime.strftime("%H:%M:%S"))
schedule.addGroupEvent(turnOnTime.hour, turnOnTime.minute, turnOnTime.second, familyRoom, 'orangeLow', 10, lightOn = True)
turnOnTime += datetime.timedelta(seconds = 5)
schedule.addGroupEvent(turnOnTime.hour, turnOnTime.minute, turnOnTime.second, familyRoom, 'relax', 50)
turnOnTime += datetime.timedelta(seconds = 5)
schedule.addGroupEvent(turnOnTime.hour, turnOnTime.minute, turnOnTime.second, familyRoom, 'reading', 50)
turnOnTime += datetime.timedelta(seconds = 5)
schedule.addGroupEvent(turnOnTime.hour, turnOnTime.minute, turnOnTime.second, familyRoom, 'relax', 50)
turnOnTime += datetime.timedelta(seconds = 5)
schedule.addGroupEvent(turnOnTime.hour, turnOnTime.minute, turnOnTime.second, familyRoom, 'orangeLow', 50)
# schedule.addEventByOffsetToLast(11, 'FamilyRoomTorch', 'relax', 5)
# schedule.addEventByOffsetToLast(11, 'FamilyRoomTorch', 'orangeLow', 5)
# schedule.addEventByOffsetToLast(11, 'FamilyRoomTorch', 'relax', 5)
# schedule.addEventByOffsetToLast(11, 'FamilyRoomTorch', 'reading', 5)
# schedule.addEventByOffsetToLast(11, 'FamilyRoomTorch', 'white', 1, lightOn = False)

# bridge = Bridge('huebridge', 'newdeveloper')
# # bridge.create_group('MasterBedroom', ["MasterBedroomHis","MasterBedroomHers"])
# bridge.get_group()
# bridge.connect()
# bridge.get_api()

# familyRoom = ["FamilyRoomTorch","FamilyRoomLeft"]

# lightsByName = bridge.get_light_objects('name')
# for light in lightsByName:
# 	print(light)

# schedules = bridge.get_schedule()
# for schedule in schedules:
# 	print(str(schedule))

# lights = bridge.get_light_objects('id')

# # Get the name of light 1, set the brightness to 127
# print(lights[1].name)
# # print(lights[1].id)

# currentConfig = {'on': True, 'hue': huelevels.HUE_ORANGE_RED, 'sat': huelevels.SAT_ORANGE_RED, 'bri': 200, 'transitiontime': 0}
# bridge.create_schedule('OrangeRedOn', getUtcTimeString(turnOnTime.hour, turnOnTime.minute, turnOnTime.second), lightsByName['FamilyRoomTorch'].light_id, currentConfig, 'OnOrangeRed')

# command =  {'transitiontime' : 10, 'on' : True, 'bri' : 0, 'hue' : huelevels.HUE_ORANGE_RED, 'sat' : huelevels.SAT_ORANGE_RED}
# bridge.set_light("FamilyRoomTorch", command)

# time.sleep(2)

# command =  {'transitiontime' : 0, 'on' : True, 'bri' : huelevels.BRI_RELAX, 'hue' : huelevels.HUE_YELLOW_SUN, 'sat' : huelevels.SAT_YELLOW_SUN}
# bridge.set_group("MasterBedroom", command)

# time.sleep(30)

# command =  {'transitiontime' : 290, 'on' : True, 'bri' : huelevels.BRI_RELAX, 'ct' : huelevels.CT_RELAX}
# bridge.set_light("FamilyRoomTorch", command)

# time.sleep(30)

# command =  {'transitiontime' : 10, 'on' : True, 'bri' : huelevels.BRI_READING, 'ct' : huelevels.CT_READING}
# bridge.set_light(familyRoom, command)

# time.sleep(30)

# command =  {'transitiontime' : 300, 'on' : True, 'bri' : huelevels.BRI_ENERGIZE, 'hue' : huelevels.HUE_WHITE, 'sat' : huelevels.SAT_WHITE}
# bridge.set_group("MasterBedroom", command)

# time.sleep(30)

# command =  {'transitiontime' : 15 * 60 * 10, 'on' : False, 'bri' : 0, 'ct' : huelevels.CT_ENERGIZE}
# bridge.set_group("All", command)
