#!/usr/bin/env ruby

require_relative 'Light'

class Group < Light
	def initialize(name)
		super(name, 0)
		@lights = Array.new;
	end

	def addLight(light)
		@lights << light
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
