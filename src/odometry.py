# !/usr/bin/env python3
"""import ev3dev.ev3 as ev3
>>> cs = ev3.ColorSensor()
>>> cs.mode = 'RGB-RAW'
>>> cs.bin_data("hhh")
(354, 415, 543)
"""

# Navigation, Koordinaten, Richtung der Strecken
# Navigation durch externe Klassen
from pickle import FALSE
import ev3dev.ev3 as ev3
from services.farbsensor import Farbsensor
from services.schallsensor import Schallsensor
from services.motor import Motor
import math
import time


class Odometry:
    colorArray = []
    farbsensor = Farbsensor()
    ultrasonic = Schallsensor()
    left = ev3.LargeMotor("outA")
    right = ev3.LargeMotor("outD")
    motor = Motor()

    paths = dict(east = False, south = True, west = False, north = False)
    directives = ['east', 'south', 'west', 'north']
    # enum 0,90,180,270
    lookDirection = 0
    leftMotor = dict(position=0)
    rightMotor = dict(position=0)
    totalDist = 0
    
    wheeldist = 14.5
    threeSixtee = 300
    distPerDegree = math.pi * 3 / threeSixtee
    
    # ki = 1
    # kd = 100
    # integral = 0
    # lastError = 0
    # derivative = 0
    
    def __init__(self):
        'return'

    def direction(self):
        alpha = 0
    
    def driving(self):
        # Farben einscannen zum kalibrieren
        loop = True
        # print(f'Start: Left: {self.leftMotor}, Right: {self.rightMotor} , Direction: {self.lookDirection  * 360 / math.pi}')
        while loop:
            if self.ultrasonic.isSomethingInMyWay():
                print('something in my way')
                # ev3.Sound.play('quak.wav')
                self.turnAround()
            
            color = self.farbsensor.recognizeColour()
            
            if color == 0:
                self.colorArray.append('blue')
                self.driveAtPoint()
                loop = False
            elif color == 1:
                self.colorArray.append('red')
                self.driveAtPoint()
                loop = False
            else:
                self.driveLine(color)
                
    def findPath(self):
        for index in range(0,4):
            self.motor.turnRight()
            time.sleep(0.5)
            while self.left.is_running:
                if self.farbsensor.isBlack():
                    self.paths[self.directives[index]] = True
        print(self.paths)
        # self.lookDirection, self.pahts, self.colorArray[self.colorArray.__len__]
        return
    
    def turnAround(self):
        self.motor.turnRight()
        time.sleep(2.5)
        self.motor.turnRight()
        time.sleep(2.5)
        
    def driveAtPoint(self):
        self.motor.tare()
        self.motor.driveSevenCM()
        self.findPath()
        self.totalDist = self.clacTotalDist() - 4
        posLeft = self.leftMotor.get('position') / self.threeSixtee
        posRight = self.rightMotor.get('position') / self.threeSixtee
        print(f'Total: {self.totalDist}')
        print(f'Rotation: {posLeft}, {posRight}')
        print(f'Direction: {self.lookDirection * 360 / math.pi}')
        ev3.Sound.play('bark.wav')
    
    def driveLine(self, lightValue):
        temp = self.motor.driveLine(lightValue)
        self.getCurrentDist(temp[0], temp[1])
        
    def getCurrentDist(self, left, right):
        # print(f'RelPos: {left}, {right}')
        tempLeft = -self.calcDist(left + self.leftMotor['position'])
        tempRight = -self.calcDist(right + self.rightMotor['position'])
        self.leftMotor['position'] = -left
        self.rightMotor['position'] = -right
        self.calcDirection(tempLeft, tempRight)
    
    def calcDirection(self, left, right):
        # print(f'RelDist: {left}, {right}')
        self.lookDirection += (right - left) / self.wheeldist
        # print(f'Direct: {(right - left) / self.wheeldist}')
        
    def clacTotalDist(self):
        dr = self.calcDist(self.rightMotor['position'])
        dl = self.calcDist(self.leftMotor['position'])
        return self.wheeldist * ((dr + dl) / (dr - dl) * math.sin((dr - dl) / (2 * self.wheeldist)))
        
    def calcDist(self, degree):
        return degree * self.distPerDegree
