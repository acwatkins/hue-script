require 'json'
require 'test/unit'

require_relative '../Light'
require_relative '../LightBulb'

class LightBulbTest < Test::Unit::TestCase
	LIGHT_UNDER_TEST = 1

	def setup
		@baseUri = 'http://huebridge.lan/api/newdeveloper/lights/' + LIGHT_UNDER_TEST.to_s
		@lightInitialSettings = LightBulb.new("LightBulbTest-initial", LIGHT_UNDER_TEST)
		@lightInitialSettings.getState

		@lightSetter = LightBulb.new("lightSetter", LIGHT_UNDER_TEST)
		@lightSetter.getState
		@lightSetter.isOn = true
		@lightSetter.updateState

		@lightGetter = LightBulb.new("lightGetter", LIGHT_UNDER_TEST)
		@lightGetter.getState
	end

	def teardown
		@lightInitialSettings.updateState
	end

	def getValue(key)
		jsonLight = Curl.get(@baseUri)
		parsedValue = JSON.parse(jsonLight.body_str)
		state = parsedValue['state']
		return state[key]
	end

	def testTurnOnAndOff
		initialState = getValue('on')
		assert_equal(initialState, @lightSetter.isOn)

		@lightSetter.isOn = !initialState
		@lightSetter.updateState
		
		assert_equal(!initialState, getValue('on'))
		assert_equal(!initialState, @lightSetter.isOn)

		@lightSetter.isOn = initialState
		@lightSetter.updateState

		assert_equal(initialState, getValue('on'))
		assert_equal(initialState, @lightSetter.isOn)
	end

	def testChangeColorTemperature
		initialState = getValue('ct')
		@lightSetter.getState
		assert_equal(initialState, @lightSetter.colorTemperature)

		runTest = Proc.new do |updatedColorTemperature|
			@lightSetter.colorTemperature = updatedColorTemperature
			@lightSetter.updateState
			@lightGetter.getState
		
			assert_equal(updatedColorTemperature, getValue('ct'))
			assert_equal(updatedColorTemperature, @lightGetter.colorTemperature)
		end

		runTest.call(200)
		runTest.call(400)
	end

	def testChangeBrightness
		initialState = getValue('bri')
		@lightSetter.getState
		assert_equal(initialState, @lightSetter.brightness)

		runTest = Proc.new do |updatedBrightness|
			@lightSetter.brightness = updatedBrightness
			@lightSetter.updateState
			@lightGetter.getState
		
			assert_equal(updatedBrightness, getValue('bri'))
			assert_equal(updatedBrightness, @lightGetter.brightness)
		end

		runTest.call(5)
		runTest.call(150)
	end

	def testChangeHue
		initialState = getValue('hue')
		@lightSetter.getState
		assert_equal(initialState, @lightSetter.hue)
		@lightSetter.saturation = 255

		runTest = Proc.new do |updatedValue|
			@lightSetter.hue = updatedValue
			@lightSetter.updateState
			@lightGetter.getState
		
			assert_equal(updatedValue, getValue('hue'))
			assert_equal(updatedValue, @lightGetter.hue)
		end

		runTest.call(Light::HUE_RED)
		runTest.call(Light::HUE_ORANGE)
		runTest.call(Light::HUE_YELLOW)
		runTest.call(Light::HUE_GREEN)
		runTest.call(Light::HUE_BLUE)
		runTest.call(Light::HUE_VIOLET)
	end

	def testChangeSaturation
		initialState = getValue('sat')
		@lightSetter.getState
		assert_equal(initialState, @lightSetter.saturation)
		@lightSetter.hue = Light::HUE_RED

		runTest = Proc.new do |updatedValue|
			@lightSetter.saturation = updatedValue
			@lightSetter.updateState
			@lightGetter.getState
		
			assert_equal(updatedValue, getValue('sat'))
			assert_equal(updatedValue, @lightGetter.saturation)
		end

		runTest.call(255)
		runTest.call(150)
		runTest.call(100)
	end
end
