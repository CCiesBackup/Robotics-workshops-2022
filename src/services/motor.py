#!/usr/bin/env python3

import ev3dev.ev3 as ev3
import time

class Motor(object):
    sleepTimer = 2
    seven = -310
    left = ev3.LargeMotor("outA")
    right = ev3.LargeMotor("outD")
    
    tp = 300
    kp = 600
    offset = 0.5
    error = 0
    turn = 0
    ki = 1
    
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
        self.left.position_sp = -442
        self.right.position_sp = 442
        
        self.setspeed(500, -(500))
        
        self.setCommand("run-to-rel-pos")
    
    def driveLine(self, lightValue):
        print(f'Light: {lightValue}')
        self.error = lightValue - self.offset
        print(f'Error: {self.error}')
        # self.integral -= error
        # self.derivative = error - self.lastError
        # turn = error * self.kp + self.ki * self.integral + self.kd * self.derivative
        self.turn = self.error * self.kp
        # self.lastError = error
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
    
    def test(self):
        self.setspeed(200, 200)
        self.setPositionSP(260)
        self.setCommand("run-to-rel-pos")
        
