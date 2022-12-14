#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time

class Motor(object):
    sleepTimer = 1.25
    seven = -310
    left = ev3.LargeMotor("outA")
    right = ev3.LargeMotor("outD")
    
    tp = 250
    kp = 450
    offset = 0.5
    error = 0
    lastError = 0
    turn = 0
    ki = 12
    kd = 450
    integral = 0
    derivative = 0
    ninety = 450
    valueRangeBlack = 0
    valueRangeWhite = 0
    
    
    def __init__(self):
        self.left.reset()
        self.right.reset()
        
        self.left.stop_action = "hold"
        self.right.stop_action = "hold"
        
        self.setCommand("run-forever")
    
    def driveBack(self):
        self.setPositionSP(-(self.seven / 7 * 2))
        
        self.setspeed(-self.tp, -self.tp)
        
        self.setCommand("run-to-rel-pos")
        
        time.sleep(self.sleepTimer)
    
    def driveSevenCM(self):
        self.setPositionSP(self.seven)
        
        self.setspeed(self.tp, self.tp)
        
        self.setCommand("run-to-rel-pos")
        
        time.sleep(self.sleepTimer)
    
    def turnRight(self):
        self.curve(self.ninety)
    
    def turnLeft(self):
        self.setPositionSP(self.ninety)
        self.setspeed(-500, 500)
        self.setCommand("run-to-rel-pos")
    
    def driveLine(self, lightValue):
        self.error = lightValue - self.offset
        self.integral += self.error
        self.derivative = self.error - self.lastError
        self.turn = self.error * self.kp + self.ki * self.integral + self.kd * self.derivative
        self.lastError = self.error
        powerA = self.tp - self.turn
        powerD = self.tp + self.turn
        
        self.setspeed(powerA, powerD)

        self.setCommand("run-forever")
        return [self.left.position, self.right.position]
    
    def tare(self):
        powerA = self.tp - self.turn
        powerD = self.tp + self.turn
        
        self.setspeed(powerA, powerD)

        self.setCommand("run-forever")
    
    def stop(self):
        self.left.stop()
        self.right.stop()
    
    def setCommand(self, command):
        self.left.command = command
        self.right.command = command
    
    def setspeed(self, powerA, powerB):
        self.left.speed_sp = -powerA
        self.right.speed_sp = -powerB
    
    def setPositionSP(self, position):
        self.left.position_sp = position
        self.right.position_sp = position
    
    def curve(self, position):
        self.left.position_sp = -position
        self.right.position_sp = position
        self.setspeed(500, -(500))
        
        self.setCommand("run-to-rel-pos")
    
    def setOffset(self, black, white):
        self.valueRangeBlack = black - self.offset
        self.valueRangeWhite = white - self.offset
    
    def reset(self):
        self.left.reset()
        self.right.reset()
        
        self.left.stop_action = "hold"
        self.right.stop_action = "hold"

