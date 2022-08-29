#!/usr/bin/env python3
import ev3dev.ev3 as ev3
class Schallsensor:
    us = ev3.UltrasonicSensor()
    
    def __init__(self):
        self.us.mode = "US-DIST-CM"
    
    def isSomethingInMyWay(self):
        return self.us.value() <= 150
