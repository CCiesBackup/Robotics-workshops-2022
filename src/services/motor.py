#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time

class Motor(object):
    sleepTimer = 1.25
    seven = -310
    left = ev3.LargeMotor("outA")
    right = ev3.LargeMotor("outD")
    
    tp = 250
    kp = 400
    offset = 0.5
    error = 0
    lastError = 0
    turn = 0
    ki = 10
    kd = 400
    integral = 0
    derivative = 0
    ninety = 442
    valueRangeBlack = 0
    valueRangeWhite = 0
    
    
    def __init__(self):
        self.left.reset()
        self.right.reset()
        
        self.left.stop_action = "brake"
        self.right.stop_action = "brake"
        
        self.setCommand("run-forever")
    
    def driveSevenCM(self):
        print('Fahre 7cm')
        self.setPositionSP(self.seven)
        
        self.setspeed(self.tp, self.tp)
        
        self.setCommand("run-to-rel-pos")
        
        time.sleep(self.sleepTimer)
    
    def turnRight(self):
        print('Drehe nach rechts')
        self.curve(self.ninety)
    
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
    
    def driveToDirection(self, currentDirection, destination):
        temp = ((destination - currentDirection) / 90) * self.ninety
        self.curve(temp)
    
    def curve(self, position):
        self.left.position_sp = -position
        self.right.position_sp = position
        self.setspeed(500, -(500))
        
        self.setCommand("run-to-rel-pos")
    
    def setOffset(self, black, white):
        self.valueRangeBlack = black - self.offset
        self.valueRangeWhite = white - self.offset
        print(f'Offset: {self.offset}, Range: {self.valueRangeBlack}, {self.valueRangeWhite}')
