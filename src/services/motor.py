#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time

class Motor(object):
    tp = 220
    sleepTimer = 2
    # seven = -286
    seven = -310
    left = ev3.LargeMotor("outA")
    right = ev3.LargeMotor("outD")
    
    def __init__(self):
        
        self.left.reset()
        self.right.reset()
        
        self.left.stop_action = "brake"
        self.right.stop_action = "brake"
        
        self.setCommand("run-forever")
    
    def driveSevenCM(self):
        print('Fahre 7cm')
        self.left.position_sp = self.seven
        self.right.position_sp = self.seven
        
        self.setspeed(self.tp, self.tp)
        
        self.setCommand("run-to-rel-pos")
        
        time.sleep(self.sleepTimer)
    
    def turnRight(self):
        print('Drehe nach rechts')
        self.left.position_sp = -450
        self.right.position_sp = 450
        
        self.setspeed(self.tp, -(self.tp))
        
        self.setCommand("run-to-rel-pos")
        
    def setCommand(self, command):
        self.left.command = command
        self.right.command = command
    
    def setspeed(self, powerA, powerB):
        self.left.speed_sp = -powerA
        self.right.speed_sp = -powerB
        return
    
    def driveLine(self, powerLevel):
        powerA = self.tp - powerLevel
        powerD = self.tp + powerLevel
        
        self.left.speed_sp = -(powerA)
        self.right.speed_sp = -(powerD)

        self.setCommand("run-forever")
        return [self.left.position, self.right.position]
    
    def stop(self):
        self.left.stop()
        self.right.stop()
    
    def resetPosition(self):
        self.left.position = 0
        self.right.position = 0
