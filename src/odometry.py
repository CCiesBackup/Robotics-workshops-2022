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
from typing import Tuple
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
    btn = ev3.Button()

    paths = dict(east = False, south = True, west = False, north = False)
    directives = ['east', 'south', 'west', 'north']
    # enum 0,90,180,270
    leftMotor = 0
    rightMotor = 0
    currentDirection = 0
    data = []
    coordinates = (0,0)

    destination = (0,0)
    radians = 0
    somethingInWay = False
    
    wheeldist = 15.1
    threeSixtee = 360
    distPerDegree = math.pi * 3 / threeSixtee
    
    def __init__(self, currentDirection, coordinates):
        self.currentDirection = currentDirection
        self.coordinates = coordinates
        
        # blue = self.calibration('Blau')
        # time.sleep(1)
        # red = self.calibration('Rot')
        # time.sleep(1)
        # white = self.calibration('Weiß')
        # time.sleep(1)
        # black = self.calibration('Schwarz')
        # time.sleep(1)
        # yellow = self.calibration('Gelb')
        red = (112, 31, 20)
        blue = (27, 97, 81)
        white = (163, 240, 147)
        black = (23, 34, 19)
        yellow = (108, 113, 21)
        self.farbsensor.setColors(black, blue, red, yellow)
        self.motor.setOffset(self.farbsensor.convert(black), self.farbsensor.convert(white))
        time.sleep(1)
        print(f'Schwarz: {black}, Blau: {blue}, Rot: {red}, Weiß: {white}, Yellow: {yellow}')

    def direction(self):
        alpha = self.radians / (2 * math.pi) * 360
        return self.roundToNinety(alpha)
    
    def driving(self):
        self.radians = 0
        self.destination = (0,0)
        print('Setzten Sie jetzt den Roboter an den gewünschten Punkt und drücken Sie eine Taste auf dem Roboter.')
        self.stealTime()
        loop = True
        while loop:
            if self.ultrasonic.isSomethingInMyWay():
                ev3.Sound.play('/home/robot/src/assets/quack.wav')
                self.somethingInWay = True
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
            elif color == 2:
                ev3.Sound.play('/home/robot/src/assets/quack.wav')
                self.somethingInWay = True
                self.turnAround()
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
        return
    
    def turnAround(self):
        self.motor.curve(self.motor.ninety * 2)
        time.sleep(2.25)
        
    def driveAtPoint(self):
        self.motor.tare()
        self.motor.driveSevenCM()
        self.findPath()
        ev3.Sound.beep()
        
        # calc Data
        list(map(self.setCalculatedData, self.data))
        self.destination = (self.destination[0] / 50, self.destination[1] / 50)
        self.pushData()
    
    def driveLine(self, lightValue):
        temp = self.motor.driveLine(lightValue)
        distTupel = self.getLocalDegree(temp[0], temp[1])
        self.data.append(distTupel)
    
    def getLocalDegree(self, left, right):
        tempLeft = -(left + self.leftMotor)
        tempRight = -(right + self.rightMotor)
        self.leftMotor = -left
        self.rightMotor = -right
        return (tempLeft, tempRight)
    
    def setCalculatedData(self, tupel):
        left = tupel[0]
        right = tupel[1]

        # calc radiant
        radiant = self.calcDirection(left, right)
        self.radians += radiant

        # calc s
        s = self.clacTotalDist(left, right, radiant)

        # calc x,y
        self.calcXY(s)
        return
    
    def calcDirection(self, left, right):
        dr = self.calcDist(right)
        dl = self.calcDist(left)
        return (dr - dl) / self.wheeldist
        
    def clacTotalDist(self, dr, dl, radiant):
        ds = (self.calcDist(dr) + self.calcDist(dl)) / 2
        if radiant == 0:
            return ds
        return 2 * (ds /radiant) * (radiant / 2)
        
    def calcDist(self, degree):
        return degree * self.distPerDegree
    
    def calcXY(self, s):
        x = self.destination[0]
        y = self.destination[1]
        x += s * math.cos(self.radians)
        y += s * math.sin(self.radians)
        self.destination = (x,y)
    
    def roundToNinety(self, number):
        return round(number / 90) * 90
    
    def roundToFifty(self, number):
        return round(number / 50) * 50
    
    def calibration(self, color):
        print(f'Kalibrierung der Farbe {color}.')
        print('Bitte plazieren Sie den Sensor über der entsprechenden Farbe und drücken Sie irgendeine Taste am Roboter um zu kalibrieren.')
        while not self.btn.any():
            time.sleep(0.01)
        return self.farbsensor.getRawColor()
    
    def stealTime(self):
        while not self.btn.any():
            time.sleep(0.01)
    
    def setCurrentDirection(self, direction):
        self.currentDirection = direction
    
    def setCoordinates(self, coordinates):
        self.coordinates = coordinates
    
    def pushData(self):
        grad = self.radians / (2 * math.pi) * 360
        print(f' Grad: {self.roundToNinety(grad)}, Koordinaten: {self.getTarget()}')
        self.somethingInWay = False
    
    def getTarget(self):
        tempCoord = (0,0)
        if self.currentDirection == 0:
            tempCoord = (self.coordinates[0] - self.destination[1], self.coordinates[1] + self.destination[0])
        elif self.currentDirection == 90:
            tempCoord = (self.coordinates[0] + self.destination[0], self.coordinates[1] + self.destination[1])
        elif self.currentDirection == 180:
            tempCoord = (self.coordinates[0] + self.destination[1], self.coordinates[1] - self.destination[0])
        elif self.currentDirection == 270:
            tempCoord = (self.coordinates[0] - self.destination[0], self.coordinates[1] - self.destination[1])
        return tempCoord
        
