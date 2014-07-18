#!/usr/bin/env ruby

require 'rubygems'
require 'huey'
require_relative 'hueylevels'
require 'solareventcalculator'
require 'tzinfo'

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
livingroom = Huey::Group.new(Huey::Bulb.find(1), Huey::Bulb.find(4), Huey::Bulb.find(5))
masterBedroom = Huey::Group.new(Huey::Bulb.find(2), Huey::Bulb.find(3))
adamBedroom = Huey::Bulb.find(2)
kenzieBedroom = Huey::Bulb.find(3)

# 6:00
puts "Turning lights orange red"
kenzieBedroom.update(rgb: RGB_ORANGE_RED, bri: 0, on: true)
livingroom.update(rgb: RGB_ORANGE_RED, bri: 0, on: true)
sleep(10)

# 6:00 - 6:30
puts "Livingroom: Beginning 30 min transition to yellow sun"
livingroom.update(rgb: RGB_YELLOW_SUN, bri: 200, transitiontime: 17900)
sleep(1800)

# 6:30 - 6:35
puts "Livingroom: Beginning 5 minute transition to white light"
livingroom.update(rgb: '#FFFFFF', bri: BRI_CONCENTRATE, transitiontime: 2900)
kenzieBedroom.update(on: false)
sleep(300)

# 6:35 - 6:40
puts "Livingroom: Beginning 5 minute transition to Energize"
livingroom.update(ct: CT_ENERGIZE, bri: BRI_ENERGIZE, transitiontime: 2901)
sleep(300)

# 6:40 - 7:00
puts "sleeping 20 minutes"
sleep(1200)

# 7:00
puts "MasterBedroom: Turning lights orange red"
masterBedroom.update(rgb: RGB_ORANGE_RED, bri: 0, on: true)
sleep(10)

# 7:00 - 7:30
puts "MasterBedroom: Beginning 30 min transition to yellow sun"
masterBedroom.update(rgb: RGB_YELLOW_SUN, bri: 200, transitiontime: 17900)
sleep(1800)

# 7:30 - 7:35
puts "MasterBedroom: Beginning 5 minute transition to white light"
masterBedroom.update(rgb: '#FFFFFF', bri: BRI_CONCENTRATE, transitiontime: 2900)
sleep(300)

# 7:35 - 7:40
puts "MasterBedroom: Beginning 5 minute transition to Energize"
masterBedroom.update(ct: CT_ENERGIZE, bri: BRI_ENERGIZE, transitiontime: 2901)
sleep(300)

sleepOffsetAfterSunrise(60 * 60)

puts "Beginning 30 min transition to off"
allLights.update(bri: 0, transitiontime:17900)
sleep(1800)

puts "Turning off lights"
allLights.update(on: false)
