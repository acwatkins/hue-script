#!/usr/bin/env ruby

require 'rubygems'
require 'huey'
require_relative 'hueLevels.rb'
require_relative 'Home.rb'

home = Home.new

# 5:45
puts "Turning lights orange red"
home.masterBedroom.update(on: true, rgb: RGB_ORANGE_RED, bri: 0)
sleep(10)

# 5:45 - 6:10
puts "Beginning 25 min transition to yellow sun"
home.masterBedroom.update(rgb: RGB_YELLOW_SUN, bri: BRI_RELAX, transitiontime: 24 * 60 * 10)
sleep(25 * 60)

# 6:10 - 6:11
puts "Beginning 1 min transition to Relax"
home.masterBedroom.update(ct: CT_RELAX, bri: BRI_RELAX, transitiontime: 50 * 10)
sleep(60)

# 6:11 - 6:13
puts "Beginning 2 min transition to Reading"
home.masterBedroom.update(ct: CT_READING, bri: BRI_READING, transitiontime: 110 * 10)
sleep(2 * 60)

# 6:13 - 6:14
puts "Beginning 1 minute transition to white light"
home.masterBedroom.update(rgb: '#FFFFFF', bri: BRI_CONCENTRATE, transitiontime: 50 * 10)
sleep(60)

# 6:14 - 6:15
puts "Beginning 1 minute transition to Energize"
home.masterBedroom.update(ct: CT_ENERGIZE, bri: BRI_ENERGIZE, transitiontime: 51 * 10)
sleep(60)
