#!/usr/bin/env python3
#-- coding: utf-8 --
import RPi.GPIO as GPIO
import time
from Car.Constants import *


#Set function to calculate percent from angle
def angle_to_percent (angle) :
    if angle > 180 or angle < 0 :
        return False
    start = 4
    end = 12.5
    ratio = (end - start)/180 #Calculate ratio from angle to percent
    angle_as_percent = angle * ratio

    return start + angle_as_percent

def controlServo (pin, degree, duration=1):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    pwm_gpio = pin
    frequence = 50
    GPIO.setup(pwm_gpio, GPIO.OUT)
    pwm = GPIO.PWM(pwm_gpio, frequence)

    pwm.start(angle_to_percent(degree*10))
    time.sleep(duration)
    pwm.start(angle_to_percent(90))

    #Close GPIO & cleanup
    pwm.stop()
    GPIO.cleanup()

def move(speed,acc,action):
    if action == "left":
        controlServo(LEFTPIN,90 + speed,acc)
        controlServo(RIGHTPIN,90 + speed,acc)
    elif action == "right":
        controlServo(LEFTPIN, 90 - speed, acc)
        controlServo(RIGHTPIN, 90 - speed, acc)
    elif action == "front":
        controlServo(LEFTPIN, 90 + speed, acc)
        controlServo(RIGHTPIN, 90 - speed, acc)
    elif action == "back":
        controlServo(LEFTPIN, 90 - speed, acc)
        controlServo(RIGHTPIN, 90 + speed, acc)