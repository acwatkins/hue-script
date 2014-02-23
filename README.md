\#hue-script

A ruby script used to control Philips Hue

## LightBulb

This is a class for controlling a single light, properties are sent to the light with updateState and retrieved from the light with getState

Usage:

> myLight = LightBulb.new("name", index)
> myLight.brightness = 200
> myLight.colorTemperature = Light::CT_READING
> myLight.isOn = true
>
> myLight.updateState

The above sets the properties of interest and sends them all to the light with updateState.  Note CT_READING, this is a constant mirroing the values supplied by philips.  You may also specify a valid number.  Another way to specify color is using hue and saturation.  [x,y] is currently not implemented.

## Group

Lights can be grouped together to send a command to all of them at once.

> myGroup = Group.new("GroupName")
> myGroup.addLight(LightBulb.new("light1", 1)
> myGroup.addLight(LightBulb.new("light2", 2)
>
> myGroup.brightness = 150
> myGroup.hue = Light::HUE_RED
> myGroup.saturation = 245
> myGroup.isOn = true
>
> myGroup.updateState 
