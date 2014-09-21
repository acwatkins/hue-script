#!/usr/bin/env ruby

require 'rubygems'
require 'huey'

class Home
	def initialize()
		@allLights = Huey::Bulb.all
		@familyRoomTorch = Huey::Bulb.find(1)
		@masterBedroomHis = Huey::Bulb.find(2)
		@masterBedroomHers = Huey::Bulb.find(3)
		@familyRoomRight = Huey::Bulb.find(4)
		@familyRoomLeft = Huey::Bulb.find(5)
		
		@familyRoom = Huey::Group.new(@familyRoomTorch, @familyRoomRight, @familyRoomLeft)
		@masterBedroom = Huey::Group.new(@masterBedroomHis, @masterBedroomHers)
	end
	
	def allLights
		@allLights
	end
	
	def familyRoomTorch
		@familyRoomTorch
	end
	
	def familyRoomRight
		@familyRoomRight
	end
	
	def familyRoomLeft
		@familyRoomLeft
	end
	
	def masterBedroomHis
		@masterBedroomHis
	end
	
	def masterBedroomHers
		@masterBedroomHers
	end
	
	def familyRoom
		@familyRoom
	end
	
	def masterBedroom
		@masterBedroom
	end
end
