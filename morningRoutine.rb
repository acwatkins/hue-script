#!/usr/bin/env ruby

require 'rubygems'
require 'huey'
require_relative 'hueylevels'
require 'solareventcalculator'
require 'tzinfo'

#module Huey
#	class CommandLine
#		def parse
#			optParser = OptionParser.new do |opts|
#			opts.banner = "Usage: huey [options]"
#
#			opts.separator ""
#
#			opts.on("-l", "--light INDEX", "Specify the light to control with its index") do |lib|
#				options.library << lib
#			end
#		end
#	end
#end

def sleepOffsetAfterSunrise(offsetInSeconds)
	latitude = BigDecimal.new("28.538335")
	longitude = BigDecimal.new("-81.379236")

	currentDate = Date.today
	solarCalculator = SolarEventCalculator.new(currentDate, latitude, longitude)
	sunriseDateTime = solarCalculator.compute_official_sunrise("America/New_York")

	currentTime = Time.now
	sunriseTime = sunriseDateTime.to_time
	timeToSleep = sunriseTime - currentTime + offsetInSeconds
	if timeToSleep > 0
		puts "Sleeping " << timeToSleep.to_s << " seconds"
		sleep(timeToSleep)
	else
		puts "Not sleeping negative amount on sunrise calculation, value: " << timeToSleep.to_s << " seconds"
	end
end

allLights = Huey::Bulb.all
livingRoom = Huey::Group.new(Huey::Bulb.find(1), Huey::Bulb.find(4), Huey::Bulb.find(5))
masterBedroom = Huey::Group.new(Huey::Bulb.find(2), Huey::Bulb.find(3))

puts "Turning lights orange red"
allLights.update(rgb: RGB_ORANGE_RED, bri: 0, on: true)
sleep(10)

puts "Beginning 30 min transition to yellow sun"
allLights.update(rgb: RGB_YELLOW_SUN, bri: 200, transitiontime: 17900)
#allLights.update(rgb: RGB_YELLOW_SUN, bri: 200, transitiontime: 600)

sleep(1800)
#sleep(70)

puts "Beginning 5 minute transition to white light"
allLights.update(rgb: '#FFFFFF', bri: BRI_CONCENTRATE, transitiontime: 2900)
sleep(300)

puts "Beginning 5 minute transition to Energize"
allLights.update(ct: CT_ENERGIZE, bri: BRI_ENERGIZE, transitiontime: 2901)
sleep(300)

sleepOffsetAfterSunrise(60 * 60)

puts "Beginning 30 min transition to off"
allLights.update(bri: 0, transitiontime:17900)
sleep(1800)

puts "Turning off lights"
allLights.update(on: false)
