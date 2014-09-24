#!/usr/bin/env ruby

require 'rubygems'
require 'huey'
require_relative 'hueLevels.rb'
require_relative 'Home.rb'

home = Home.new

# 9:30 - 10:00
puts "Beginning 30 min transition to yellow sun"
home.allLights.update(rgb: RGB_YELLOW_SUN, bri: BRI_RELAX, transitiontime: 29 * 60 * 10)
sleep(30 * 60)

# 10:00 - 10:05
puts "Beginning 5 min transition to orange red low light"
home.allLights.update(rgb: RGB_ORANGE_RED, bri: 0, transitiontime: 4 * 60 * 10)
sleep(5 * 60)

# 10:05 - 10:15
sleep(10 * 60)
puts "Turning off lights"
home.allLights.update(on: false)
