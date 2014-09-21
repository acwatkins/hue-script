#!/usr/bin/env ruby

require 'rubygems'
require 'huey'
require_relative 'hueLevels.rb'
require_relative 'Home.rb'

home = Home.new

# 5:45
puts "Turning lights orange red"
home.familyRoom.update(on: true, rgb: RGB_ORANGE_RED, bri: 0)
sleep(10)

# 5:45 - 6:30
puts "Beginning 45 min transition to yellow sun"
home.familyRoom.update(rgb: RGB_YELLOW_SUN, bri: BRI_RELAX, transitiontime: 44 * 60 * 10)
sleep(45 * 60)

# 6:30 - 6:45
home.familyRoom.update(ct: CT_RELAX, bri: BRI_RELAX, transitiontime: 14 * 60 * 10)
sleep(15 * 60)

# 6:45 - 7:05
home.familyRoom.update(ct: CT_READING, bri: BRI_READING, transitiontime: 9 * 60 * 10)
sleep(20 * 60)

# 7:05 - 7:10
home.familyRoom.update(rgb: RGB_WHITE, bri: BRI_CONCENTRATE, transitiontime: 4 * 60 * 10)
sleep(5 * 60)

# 7:10 - 7:12
home.familyRoom.update(rgb: RGB_CLOUDY_SKY, bri: BRI_ENERGIZE, transitiontime: 2 * 60 * 10)
sleep(2 * 60)

# 7:12 - 7:15
home.familyRoom.update(rgb: RGB_BLUE_SKY, bri: BRI_ENERGIZE, transitiontime: 3 * 60 * 10)
