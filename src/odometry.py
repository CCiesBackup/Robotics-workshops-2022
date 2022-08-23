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
    kp = 600
    offset = 0.5
    error = 0
    turn = 0
    paths = dict(east = False, south = True, west = False, north = False)
    directives = ['east', 'south', 'west', 'north']
    # enum 0,90,180,270
    lookDirection = 0
    leftMotor = dict(position=0, distance=0)
    rightMotor = dict(position=0, distance=0)
    wheeldist = 14.5
    threeSixtee = 260
    # Anpassen (50 -> 55 - 56, 100 -> 126[f]) 0,12 - 0,26 pro CM
    distPerDegree = 3 * math.pi / threeSixtee
    totalDist = 0
    
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
        loop = True
        print(f'Start: Left: {self.leftMotor}, Right: {self.rightMotor} , Direction: {self.lookDirection  * 360 / math.pi}')
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
        # print(f'End: Left: {self.leftMotor['distance']}, Right: {self.rightMotor['distance']} , Direction: {self.lookDirection  * 360 / math.pi}')
                
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
        self.motor.driveLine(-(self.turn))
        # self.motor.driveLine(-(self.turn))
        self.motor.driveSevenCM()
        self.findPath()
        self.clacTotalDist()
        posLeft = self.leftMotor.get('position') / self.threeSixtee
        posRight = self.rightMotor.get('position') / self.threeSixtee
        print(f'Total: {self.totalDist}')
        print(f'Rotation: {posLeft}, {posRight}')
        print(f'Direction: {self.lookDirection * 360 / math.pi}')
        ev3.Sound.play('bark.wav')
    
    def driveLine(self, lightValue):
        self.error = lightValue - self.offset
        # self.integral -= error
        # self.derivative = error - self.lastError
        # turn = error * self.kp + self.ki * self.integral + self.kd * self.derivative
        self.turn = self.error * self.kp
        temp = self.motor.driveLine(self.turn)
        self.getCurrentDist(temp[0], temp[1])
        # print(f'Left: {self.leftMotor['distance']}, Right: {self.rightMotor['distance']} , Direction: {self.lookDirection  * 360 / math.pi}')
        # self.lastError = error
        
    def getCurrentDist(self, left, right):
        print(f'RelPos: {left}, {right}')
        tempLeft = -self.calcDist(left + self.leftMotor['position'])
        tempRight = -self.calcDist(right + self.rightMotor['position'])
        self.leftMotor['position'] = -left
        self.rightMotor['position'] = -right
        self.leftMotor['distance'] += tempLeft
        self.rightMotor['distance'] += tempRight
        self.calcDirection(tempLeft, tempRight)
    
    def calcDirection(self, left, right):
        print(f'RelDist: {left}, {right}')
        self.lookDirection += (right - left) / self.wheeldist
        print(f'Direct: {(right - left) / self.wheeldist}')
        
    def clacTotalDist(self):
        self.totalDist = self.wheeldist * (self.calcDist(self.rightMotor['position']) + self.calcDist(self.leftMotor['position'])) / (self.calcDist(self.rightMotor['position']) - self.calcDist(self.leftMotor['position'])) * math.sin((self.calcDist(self.rightMotor['position']) - self.calcDist(self.leftMotor['position'])) / (2 * self.wheeldist))
        
    def calcDist(self, degree):
        return degree * self.distPerDegree
