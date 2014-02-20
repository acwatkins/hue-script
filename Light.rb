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

	def initialize(name, index)
		@name = name
		@index = index
		@brightness = 200
		@colorTemperature = CT_READING
		@isOn = false
	end

	def name
		@name
	end

	def isOn=(value)
		@isOn = value
	end

	def colorTemperature=(value)
		@colorTemperature = value
	end

	def brightness=(value)
		@brightness = value
	end
end
