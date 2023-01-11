#!/usr/bin/python
import RPi.GPIO as GPIO
import time
# paragem 1 - entrada de alunos
LED1_PIN = 11 #P1 - pede boleia e acende o LED1
LED2_PIN = 13 #P2 - pede boleia e acende o LED2
LED3_PIN = 15 #P3
# paragem 2 - entrada de alunos
LED4_PIN = 29 #P1
LED5_PIN = 31 #P2
LED6_PIN = 33 #P3 - pede boleia e acende o LED6
# paragem 3 - School
LED7_PIN = 36 #P1
LED8_PIN = 38 #P2
LED9_PIN = 40 #P3

#GPIO numbering scheme 
#BOARD - pin numbers of the Pi header
#BMC   - GPIO numbers (depends on the Raspberry PI version)
GPIO.setmode(GPIO.BOARD)

#GPIO channel setup
#IN  - input
#OUT - output
GPIO.setup(LED1_PIN,GPIO.OUT)
GPIO.setup(LED2_PIN,GPIO.OUT)
GPIO.setup(LED3_PIN,GPIO.OUT)
GPIO.setup(LED4_PIN,GPIO.OUT)
GPIO.setup(LED5_PIN,GPIO.OUT)
GPIO.setup(LED6_PIN,GPIO.OUT)
GPIO.setup(LED7_PIN,GPIO.OUT)
GPIO.setup(LED8_PIN,GPIO.OUT)
GPIO.setup(LED9_PIN,GPIO.OUT)

#GPIO channel state
#HIGH  - True or 1
#LOW   - False or 0
for i in range(1):
    # pedidos de boleia
    GPIO.output(LED1_PIN,GPIO.HIGH)
    GPIO.output(LED2_PIN,GPIO.HIGH)
    GPIO.output(LED3_PIN,GPIO.LOW)
    GPIO.output(LED4_PIN,GPIO.LOW)
    GPIO.output(LED5_PIN,GPIO.LOW)
    GPIO.output(LED6_PIN,GPIO.HIGH)
    GPIO.output(LED7_PIN,GPIO.LOW)
    GPIO.output(LED8_PIN,GPIO.LOW)
    GPIO.output(LED9_PIN,GPIO.LOW)
    time.sleep(5)
    # P1 e P2 entra no OBU e começa a viagem
    GPIO.output(LED1_PIN,GPIO.LOW)
    GPIO.output(LED2_PIN,GPIO.LOW)
    time.sleep(10)
    # P2 entra no OBU e começa a viagem
    GPIO.output(LED6_PIN,GPIO.LOW)
    time.sleep(15)
    # chegada na escola
    GPIO.output(LED7_PIN,GPIO.HIGH)
    GPIO.output(LED8_PIN,GPIO.HIGH)
    GPIO.output(LED9_PIN,GPIO.HIGH)
    time.sleep(5)
GPIO.cleanup()