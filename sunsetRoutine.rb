#!/usr/bin/env ruby

require 'rubygems'
require 'huey'
require_relative 'hueLevels.rb'
require_relative 'OrlandoSolarCalculator.rb'
require_relative 'Home.rb'

puts "Sleeping before sunset"
solarCalculator = OrlandoSolarCalculator.new
solarCalculator.sleepOffsetBeforeSunset(90 * 60)

# 1.5 hours before sunset
puts "Turning on lights"
home = Home.new
home.allLights.update(on: true, rgb: RGB_BLUE_SKY, bri: 0)
sleep(10)

puts "Beginning 30 min transition increasing brightness"
home.allLights.update(rgb: RGB_BLUE_SKY, bri: BRI_ENERGIZE, transitiontime: 30 * 60 * 10)

# sunset
puts "Sleeping until sunset: " << solarCalculator.getSecondsUntilSunset().to_s << " seconds"
if (solarCalculator.getSecondsUntilSunset() > 0)
	sleep(solarCalculator.getSecondsUntilSunset())
end

puts "Beginning 3 min transition to cloudy sky"
home.allLights.update(rgb: RGB_CLOUDY_SKY, bri: BRI_CONCENTRATE, transitiontime: 3 * 60 * 10)
sleep((3 * 60) + 10)

secondsToTransition = solarCalculator.getSecondsUntilCivilSunset().to_i - 10
puts "Beginning transition to white for " << secondsToTransition.to_s << " seconds"
home.allLights.update(rgb: RGB_WHITE, bri: BRI_CONCENTRATE, transitiontime: secondsToTransition.to_i * 10)

# civil sunset
puts "Sleeping until civil sunset"
if (solarCalculator.getSecondsUntilCivilSunset() > 0)
	sleep(solarCalculator.getSecondsUntilCivilSunset())
end
secondsToTransition = solarCalculator.getSecondsUntilNauticalSunset()
puts "Beginning " << secondsToTransition.to_s << " second transition to reading"
home.allLights.update(ct: CT_READING, bri: BRI_READING, transitiontime: secondsToTransition.to_i * 10)

# nautical sunset
puts "Sleeping until nautical sunset"
if (solarCalculator.getSecondsUntilNauticalSunset() > 0)
	sleep(solarCalculator.getSecondsUntilNauticalSunset())
end	
puts "Beginning 1 hour transition to relax"
home.allLights.update(ct: CT_RELAX, bri: BRI_RELAX, transitiontime: 60 * 60 * 10)
