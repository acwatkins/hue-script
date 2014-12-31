#!/usr/bin/env python3

import datetime
import huelevels
import pytz
import time
from astral import Astral
from phue import Bridge

import logging
logging.basicConfig()

bridge = Bridge('huebridge', 'newdeveloper')
bridge.create_group('MasterBedroom', ["MasterBedroomHis","MasterBedroomHers"])
bridge.get_group()
# bridge.connect()
# bridge.get_api()

familyRoom = ["FamilyRoomTorch","FamilyRoomLeft"]

lightsByName = bridge.get_light_objects('name')
for light in lightsByName:
	print(str(light))

schedules = bridge.get_schedule()
for schedule in schedules:
	print(str(schedule))

currentConfig = {'on': True, 'hue': huelevels.HUE_ORANGE_RED, 'sat': huelevels.SAT_ORANGE_RED, 'bri': 200, 'transitiontime': 0}
bridge.create_schedule('OrangeRedOn', "2014-12-20T21:55:00", familyRoom, currentConfig, 'OnOrangeRed')

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
