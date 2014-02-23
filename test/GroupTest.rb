#!/usr/bin/env ruby

require 'minitest/autorun'
require_relative 'LightBulbStub'
require_relative '../Group'

class GroupTest < MiniTest::Unit::TestCase
	def setup
		@group = Group.new("Test Group")
		@light1 = LightBulbStub.new
		@light2 = LightBulbStub.new
		@group.addLight(@light1)
		@group.addLight(@light2)

		@group.isOn = true
		@light1.updateStateCalled = false
		@light2.updateStateCalled = false
	end

	def test_ChangeStateUsingColorTemperature
		@group.brightness = 123
		@group.colorTemperature = 456
		@group.updateState

		assert_equal(@group.isOn, @light1.isOn)
		assert_equal(@group.isOn, @light2.isOn)
		assert_equal(@group.brightness, @light1.brightness)
		assert_equal(@group.brightness, @light2.brightness)
		assert_equal(@group.colorTemperature, @light1.colorTemperature)
		assert_equal(@group.colorTemperature, @light2.colorTemperature)
		
		assert_equal(true, @light1.updateStateCalled)
		assert_equal(true, @light2.updateStateCalled)
	end

	def testChangeStateUsingHueAndSaturation
		@group.brightness = 200
		@group.hue = Light::HUE_GREEN
		@group.saturation = 223
		@group.updateState

		assert_equal(@group.isOn, @light1.isOn)
		assert_equal(@group.isOn, @light2.isOn)
		assert_equal(@group.brightness, @light1.brightness)
		assert_equal(@group.brightness, @light2.brightness)
		assert_equal(@group.hue, @light1.hue)
		assert_equal(@group.hue, @light2.hue)
		assert_equal(@group.saturation, @light1.saturation)
		assert_equal(@group.saturation, @light2.saturation)
		
		assert_equal(true, @light1.updateStateCalled)
		assert_equal(true, @light2.updateStateCalled)
	end
end
