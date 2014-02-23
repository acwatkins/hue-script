#!/usr/bin/env ruby

require 'json'

class LightBulb < Light
	def initialize(name, index)
		super(name, index)
		@baseUri = 'http://huebridge.lan/api/newdeveloper/lights/'
                @baseUri << @index.to_s
	end

	def getState
		jsonReturn = Curl.get(@baseUri)
		parsedValue = JSON.parse(jsonReturn.body_str)
		state = parsedValue['state']
		@isOn = state['on']
		@colorTemperature = state['ct']
		@brightness = state['bri']
		@hue = state['hue']
		@saturation = state['sat']
	end

	def updateState
		if @isOn
			if @colorTemperature != nil
				jsonReturn = Curl.put(@baseUri + "/state",
					{"on" => @isOn,"bri" => @brightness.to_i,
					"ct" => @colorTemperature}.to_json)
				puts jsonReturn.body_str
			elsif @hue != nil
				jsonReturn = Curl.put(@baseUri + "/state",
					{"on" => @isOn,"bri" => @brightness.to_i,
					"hue" => @hue,"sat" => @saturation}.to_json)
				puts jsonReturn.body_str
			end
		else
			jsonReturn = Curl.put(@baseUri + "/state",
				{"on" => @isOn}.to_json)
			puts jsonReturn.body_str
		end
        end
end
