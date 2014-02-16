#!/usr/bin/env ruby

class LightBulb < Light
	def initialize(name, index)
		super(name, index)
		@baseUri = 'http://huebridge.lan/api/newdeveloper/lights/'
                @baseUri << @index.to_s
	end

	def updateState
                http = Curl.put(@baseUri + "/state",
                        {"on" => @isOn,"bri" => @brightness.to_i,"ct" => @colorTemperature}.to_json)
                puts http.body_str
        end
end
