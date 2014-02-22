#!/usr/bin/env ruby

require 'rubygems'
require 'curl'
require 'rest_client'
require 'json'
require 'base64'

class Light
	CT_READING = 343
	CT_RELAX = 467
	CT_ENERGIZE = 155
	CT_CONCENTRATE = 234
	HUE_RED = 0
	HUE_ORANGE = 6375
	HUE_YELLOW = 12750
	HUE_GREEN = 36210
	HUE_BLUE = 46920
	HUE_VIOLET = 56100

	def initialize(name, index)
		@name = name
		@index = index
		@brightness = 200
		@colorTemperature = CT_READING
		@hue = nil
		@saturation = 255
		@isOn = false
	end

	def name
		@name
	end

	def isOn
		@isOn
	end

	def isOn=(value)
		@isOn = value
	end

	def colorTemperature
		@colorTemperature
	end

	def colorTemperature=(value)
		@colorTemperature = value
		@hue = nil
	end

	def brightness
		@brightness
	end

	def brightness=(value)
		@brightness = value
	end

	def hue=(value)
		@hue = value
		@colorTemperature = nil
	end

	def hue
		@hue
	end

	def saturation=(value)
		@saturation = value
	end

	def saturation
		@saturation
	end
end
