#!/usr/bin/env ruby

require_relative 'Light'

class Room
	def initialize
		@lights = Array.new;
	end

	def addLight(light)
		@lights << light
	end

	def isOn=(value)
		@isOn = value
	end

	def brightness=(value)
		@brightness = value
	end
	
	def colorTemperature=(value)
		@colorTemperature = value
	end

	def updateState
		for light in @lights
			light.isOn = @isOn
			light.brightness = @brightness
			light.colorTemperature = @colorTemperature
			light.updateState
		end
	end
end
