#!/usr/bin/env python
# #################################################
## FFUNCTIONS USED IN AU - LED control
#################################################

#!/usr/bin/python
import RPi.GPIO as GPIO
import time
LED1_PIN = 11
GPIO.setup(LED1_PIN,GPIO.OUT)

def led_activation(isOn):
    if(isOn):
        GPIO.output(LED1_PIN,GPIO.HIGH)
    else:
        GPIO.output(LED1_PIN,GPIO.LOW)