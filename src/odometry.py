# !/usr/bin/env python3
"""import ev3dev.ev3 as ev3
>>> cs = ev3.ColorSensor()
>>> cs.mode = 'RGB-RAW'
>>> cs.bin_data("hhh")
(354, 415, 543)
"""

# Navigation, Koordinaten, Richtung der Strecken
# Navigation durch externe Klassen
import ev3dev.ev3 as ev3
from services.farbsensor import Farbsensor
from services.motor import Motor
import time


class Odometry:
    colorArray = []
    motor = Motor()
    farbsensor = Farbsensor()
    left = ev3.LargeMotor("outA")
    right = ev3.LargeMotor("outD")
    kp = 600
    offset = 0.5
    cs = ev3.ColorSensor()
    error = 0
    turn = 0
    paths = dict(east = False, south = True, west = False, north = False)
    directives = ['east', 'south', 'west', 'north']
    # enum 0,90,180,270
    lookDirection = 0
    # ki = 1
    # kd = 100
    # integral = 0
    # lastError = 0
    # derivative = 0
    
    def __init__(self):
        self.left.reset()
        self.right.reset()
        
        self.left.stop_action = "brake"
        self.right.stop_action = "brake"
        
        self.left.command = "run-forever"
        self.right.command = "run-forever"
        
        self.cs.mode = "RGB-RAW"

    def direction(self):
        alpha = 0
    
    def driving(self):
        loop = True
        while loop:
            # print(self.cs.bin_data("hhh"))
            # Ultrashallsensor testet, ob etwas im Weg ist
                # 180° Drehung
            color = self.farbsensor.recognizeColour()
            
            if color == 1:
                self.colorArray.append('blue')
                self.driveAtPoint()
                loop = False
            elif color == 2:
                self.colorArray.append('blue')
                self.driveAtPoint()
                loop = False
            else:
                self.driveLine(color)
            # if self.farbsensor.isBlue() | self.farbsensor.isRed():
            #     if self.farbsensor.isBlue():
            #         self.colorArray.append('blue')
            #     else:
            #         self.colorArray.append('red')
            #     self.driveAtPoint()
            #     # Daten schicken
            #     # warten
            #     loop = False
            # else:
            #     self.driveLine()
                
    def findPath(self):
        for index in range(0,4):
            self.motor.turnRight(self.left,self.right)
            while self.left.is_running:
                if self.farbsensor.isBlack():
                    self.paths[self.directives[index]] = True
        print(self.paths)
        # self.lookDirection, self.pahts, self.colorArray[self.colorArray.__len__]
        return
    
    def turnAround(self):
        self.motor.turnRight(self.left,self.right)
        self.motor.turnRight(self.left,self.right)
        
    def driveAtPoint(self):
        self.motor.driveLine(-(self.turn), self.left, self.right)
        self.motor.driveLine(-(self.turn), self.left, self.right)
        self.motor.driveSevenCM(self.left,self.right)
        self.findPath()
    
    def driveLine(self, lightValue):
        self.error = lightValue - self.offset
        # self.integral -= error
        # self.derivative = error - self.lastError
        # turn = error * self.kp + self.ki * self.integral + self.kd * self.derivative
        self.turn = self.error * self.kp
        self.motor.driveLine(self.turn, self.left, self.right)
        # self.lastError = error
