#!/usr/bin/env ruby

require 'rubygems'
require 'huey'
require_relative 'hueylevels'
require 'solareventcalculator'
require 'tzinfo'

allLights = Huey::Bulb.all
livingRoom = Huey::Group.new(Huey::Bulb.find(1), Huey::Bulb.find(4), Huey::Bulb.find(5))
masterBedroom = Huey::Group.new(Huey::Bulb.find(2), Huey::Bulb.find(3))

# 8:30 - 8:31
puts "Beginning 1 minute transition to white light"
allLights.update(rgb: '#FFFFFF', bri: BRI_CONCENTRATE, transitiontime: 500)
sleep(60)

# 8:31
puts "Beginning 4 minute transition to reading"
allLights.update(ct: CT_READING, bri: BRI_READING, transitiontime: 2300)

# 8:31 - 9:00
sleep(1740)

#9:00 - 9:30
puts "Beginning 30 min transition to relax"
allLights.update(ct: CT_RELAX, bri: BRI_RELAX, transitiontime: 17900)
sleep(900)
puts "15 more minutes in transition"
sleep(900)

#9:30 - 9:45
puts "Beginning 15 min transition to yellow sun"
allLights.update(rgb: RGB_YELLOW_SUN, bri: BRI_RELAX, transitiontime: 8900)
sleep(900)

#9:45 - 10:15
puts "Beginning 30 min transition to orange red"
allLights.update(rgb: RGB_ORANGE_RED, bri: 0, transitiontime: 17900)
sleep(900)
puts "15 more minutes in transition"
sleep(900)

#10:15 - 10:30
sleep(900)
puts "Turning off lights"
allLights.update(on: false)

