#!/usr/bin/env ruby

require 'rubygems'
require 'solareventcalculator'
require 'tzinfo'

class OrlandoSolarCalculator
	def initialize()
		@latitude = BigDecimal.new("28.538335")
		@longitude = BigDecimal.new("-81.379236")
		@timezone = "America/New_York"
		@currentDate = Date.today
		@solarCalculator = SolarEventCalculator.new(@currentDate, @latitude, @longitude)
	end
	
	def getSunrise()
		sunriseDateTime = @solarCalculator.compute_official_sunrise(@timezone)
	end
	
	def getSecondsUntilSunrise()
		seconds = getSecondsUntilDateTime(getSunrise())
	end

	def getSunset()
		sunsetDateTime = @solarCalculator.compute_official_sunset(@timezone)
	end
		
	def getSecondsUntilSunset()
		seconds = getSecondsUntilDateTime(getSunset())
	end

	def getCivilSunrise()
		sunriseDateTime = @solarCalculator.compute_civil_sunrise(@timezone)
	end

	def getSecondsUntilCivilSunrise()
		seconds = getSecondsUntilDateTime(getCivilSunrise())
	end
	
	def getCivilSunset()
		sunsetDateTime = @solarCalculator.compute_civil_sunset(@timezone)
	end

	def getSecondsUntilCivilSunset()
		seconds = getSecondsUntilDateTime(getCivilSunset())
	end

	def getNauticalSunrise()
		sunriseDateTime = @solarCalculator.compute_nautical_sunrise(@timezone)
	end

	def getSecondsUntilNauticalSunrise()
		seconds = getSecondsUntilDateTime(getNauticalSunrise())
	end
	
	def getNauticalSunset()
		sunsetDateTime = @solarCalculator.compute_nautical_sunset(@timezone)
	end

	def getSecondsUntilNauticalSunset()
		seconds = getSecondsUntilDateTime(getNauticalSunset())
	end

	def sleepOffsetBeforeSunset(offsetInSeconds)
		sunsetDateTime = getSunset()
		sleepUntilTimeWithOffset(sunsetDateTime, -offsetInSeconds)
	end

	def sleepOffsetAfterSunrise(offsetInSeconds)
		sunriseDateTime = getSunrise()
		sleepUntilTimeWithOffset(sunriseDateTime, offsetInSeconds)
	end
	
	def sleepUntilCivilTwilight()
		civilTwilightDateTime = @solarCalculator.compute_official
	end
	
	def getSecondsUntilDateTime(dateTime)
		currentTime = Time.now
		time = dateTime.to_time
		timeToSleep = time - currentTime
	end
	
	def sleepUntilTimeWithOffset(dateTime, offsetInSeconds)
		timeToSleep = getSecondsUntilDateTime(dateTime) + offsetInSeconds
		if timeToSleep > 0
			puts "Sleeping " << timeToSleep.to_s << " seconds"
			sleep(timeToSleep)
		else
			puts "OrlandoSolarCalculator, Not sleeping negative amount, value: " << timeToSleep.to_s << " seconds"
		end
	end
end
