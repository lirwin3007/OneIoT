from machine import Pin, PWM

red= PWM(Pin(12))
green= PWM(Pin(13))
blue= PWM(Pin(14))

red.duty(0)
green.duty(0)
blue.duty(0)

def set_state(redValue, greenValue, blueValue):
	red.duty(int(redValue))
	green.duty(int(greenValue))
	blue.duty(int(blueValue))