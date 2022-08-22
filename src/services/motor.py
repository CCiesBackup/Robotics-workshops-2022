#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time

class Motor(object):
    tp = 200
    sleepTimer = 3
    # seven = -286
    seven = -310
    
    def __init__(self):
        """
        Initializes odometry module
        """
    
    def driveSevenCM(self, left, right):
        print('Fahre 7cm')
        left.position_sp = self.seven
        right.position_sp = self.seven
        
        self.setspeed(left, right, self.tp, self.tp)
        
        self.setCommand(left, right, "run-to-rel-pos")
        
        time.sleep(self.sleepTimer)
    
    def turnRight(self, left, right):
        print('Drehe nach rechts')
        left.position_sp = -450
        right.position_sp = 450
        
        self.setspeed(left, right, self.tp, -(self.tp))
        
        self.setCommand(left, right, "run-to-rel-pos")
        
    def setCommand(self, left, right, command):
        left.command = command
        right.command = command
    
    def setspeed(self, left, right, powerA, powerB):
        left.speed_sp = -powerA
        right.speed_sp = -powerB
        return
    
    def driveLine(self, powerLevel, left, right):
        powerA = self.tp - powerLevel
        powerD = self.tp + powerLevel
        
        left.speed_sp = -(powerA)
        right.speed_sp = -(powerD)

        self.setCommand(left, right, "run-forever")
        return
