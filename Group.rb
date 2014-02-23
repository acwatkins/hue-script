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
			if @colorTemperature != nil
				light.colorTemperature = @colorTemperature
			elsif @hue != nil
				light.hue = @hue
				light.saturation = @saturation
			end
			light.updateState
		end
	end
end
