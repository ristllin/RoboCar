#!/usr/bin/env python3
#-- coding: utf-8 --
import RPi.GPIO as GPIO
import time
from Constants import *


#Set function to calculate percent from angle
def angle_to_percent (angle) :
    if angle > 180:
        angle = 180
    elif angle < 0 :
        angle = 0
    start = 4
    end = 12.5
    ratio = (end - start)/180 #Calculate ratio from angle to percent
    angle_as_percent = angle * ratio
    return start + angle_as_percent

class MovementAgent:
    def __init__(self):
        frequence = 50
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.left_pwm_gpio = LEFTPIN
        self.right_pwm_gpio = RIGHTPIN
        GPIO.setup(self.left_pwm_gpio, GPIO.OUT)
        GPIO.setup(self.right_pwm_gpio, GPIO.OUT)
        self.left_pwm = GPIO.PWM(self.left_pwm_gpio, frequence)
        self.right_pwm = GPIO.PWM(self.right_pwm_gpio, frequence)

    def terminate(self):
        self.left_pwm.stop()
        self.right_pwm.stop()
        GPIO.cleanup()
        
    def move(self,speed,acc,action):
        speed = speed * 10
        print("movement action: ",action)
        if action == "left":
            self.left_pwm.start(angle_to_percent(ZEROANGLE+speed))
            self.right_pwm.start(angle_to_percent(ZEROANGLE+speed))
        elif action == "right":
            self.left_pwm.start(angle_to_percent(ZEROANGLE-speed))
            self.right_pwm.start(angle_to_percent(ZEROANGLE-speed))
        elif action == "front":
            self.left_pwm.start(angle_to_percent(ZEROANGLE+speed))
            self.right_pwm.start(angle_to_percent(ZEROANGLE-speed))
        elif action == "back":
            self.left_pwm.start(angle_to_percent(ZEROANGLE-speed))
            self.right_pwm.start(angle_to_percent(ZEROANGLE+speed))
        time.sleep(1)
        self.left_pwm.start(angle_to_percent(ZEROANGLE))
        self.right_pwm.start(angle_to_percent(ZEROANGLE))
    
    
    
# agent = MovementAgent()
#  
# agent.move(9,0,"front")
# time.sleep(3)
# agent.move(9,0,"back")
# time.sleep(1)
# agent.terminate()

# GPIO.setmode(GPIO.BOARD) #Use Board numerotation mode
# GPIO.setwarnings(False) #Disable warnings
# pwm_gpio = 12
# frequence = 50
# GPIO.setup(pwm_gpio, GPIO.OUT)
# pwm = GPIO.PWM(pwm_gpio, frequence)
# pwm.start(angle_to_percent(0))
# time.sleep(1)
# pwm.stop()
# GPIO.cleanup()