#!/usr/bin/env ruby

require_relative '../Light.rb'
require_relative '../LightBulb.rb'

class LightBulbStub < LightBulb
	def initialize
		@updateStateCalled = false
	end

	def updateStateCalled
		@updateStateCalled
	end

	def updateStateCalled=(value)
		@updateStateCalled = value
	end

	def updateState
		@updateStateCalled = true
	end
end
