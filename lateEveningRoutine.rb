#!/usr/bin/env ruby

require 'rubygems'
require 'huey'
require_relative 'hueylevels'
require 'solareventcalculator'
require 'tzinfo'

allLights = Huey::Bulb.all
livingRoom = Huey::Group.new(Huey::Bulb.find(1), Huey::Bulb.find(4), Huey::Bulb.find(5))
masterBedroom = Huey::Group.new(Huey::Bulb.find(2), Huey::Bulb.find(3))
adamLight = Huey::Bulb::find(2)
kenzieLight = Huey::Bulb::find(3)

# 8:30 - 8:31
puts "Beginning 1 minute transition to white light"
allLights.update(rgb: '#FFFFFF', bri: BRI_CONCENTRATE, transitiontime: 500)
sleep(60)

# 8:31
puts "Beginning 5 minute transition to reading"
allLights.update(ct: CT_READING, bri: BRI_READING, transitiontime: 2901)

# 8:31 - 9:00
sleep(1740)

# 9:00 - 9:30
puts "MasterBedroom: Beginning 30 min transition to relax"
masterBedroom.update(ct: CT_RELAX, bri: BRI_RELAX, transitiontime: 17900)
sleep(1800)

# 9:30 - 9:45
puts "MasterBedroom: Beginning 15 min transition to yellow sun"
masterBedroom.update(rgb: RGB_YELLOW_SUN, bri: BRI_RELAX, transitiontime: 8900)
sleep(900)

# 9:45 - 10:00
puts "MasterBedroom: Beginning 30 min transition to orange red"
masterBedroom.update(rgb: RGB_ORANGE_RED, bri: 0, transitiontime: 17900)
sleep(900)

# 10:00 - 10:15
puts "Livingroom: Beginning 30 min transition to relax"
puts "MasterBedroom: 15 more minutes in transition"
livingRoom.update(ct: CT_RELAX, bri: BRI_RELAX, transitiontime: 17900)
sleep(900)

# 10:15 - 10:30
puts "MasterBedroom: Transition to low red/orange light complete"
sleep(900)

# 10:30 - 10:45
puts "Turning off Kenzie's light"
kenzieLight.update(on: false)
puts "Livingroom: Beginning 15 min transition to yellow sun"
livingRoom.update(rgb: RGB_YELLOW_SUN, bri: BRI_RELAX, transitiontime: 8900)
sleep(900)

# 10:45 - 11:15
puts "Livingroom: Beginning 30 min transition to orange red"
livingRoom.update(rgb: RGB_ORANGE_RED, bri: 0, transitiontime: 17900)
sleep(1800)

# 11:15 - 11:30
puts "Waiting 15 minutes before turning off lights"
sleep(900)

# 11:30
allLights.update(on: false)
