#!/usr/bin/env ruby

require 'rubygems'
require 'huey'
require_relative 'hueylevels.rb'
require 'solareventcalculator'
require 'tzinfo'

def sleepOffsetBeforeSunset(offsetInSeconds)
	latitude = BigDecimal.new("28.538335")
	longitude = BigDecimal.new("-81.379236")

	currentDate = Date.today
	solarCalculator = SolarEventCalculator.new(currentDate, latitude, longitude)
	sunsetDateTime = solarCalculator.compute_official_sunset("America/New_York")

	currentTime = Time.now
	sunsetTime = sunsetDateTime.to_time
	timeToSleep = sunsetTime - currentTime - offsetInSeconds
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

puts "Sleeping before sunset"
sleepOffsetBeforeSunset(90 * 60)

puts "Turning on lights"
allLights.update(ct: CT_ENERGIZE, bri: 0, on: true)
sleep(10)

puts "Beginning 30 min transition increasing brightness"
allLights.update(ct: CT_ENERGIZE, bri: BRI_ENERGIZE, transitiontime: 17900)
