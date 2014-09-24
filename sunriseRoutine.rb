#!/usr/bin/env ruby

require 'rubygems'
require 'huey'
require_relative 'hueLevels.rb'
require_relative 'OrlandoSolarCalculator.rb'
require_relative 'Home.rb'

solarCalculator = OrlandoSolarCalculator.new
solarCalculator.sleepOffsetAfterSunrise(60 * 60)

home = Home.new
puts "Beginning 30 min transition to off"
home.allLights.update(bri: 0, transitiontime: 29 * 60 * 10)
sleep(30 * 60)

puts "Turning off lights"
home.allLights.update(on: false)
