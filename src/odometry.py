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
    radians = 0
    leftMotor = dict(position=0)
    rightMotor = dict(position=0)
    totalDist = 0
    currentDirection = 0
    coordinates = (0,0)
    
    wheeldist = 14.5
    threeSixtee = 360
    distPerDegree = math.pi * 3 / threeSixtee
    
    # ki = 1
    # kd = 100
    # integral = 0
    # lastError = 0
    # derivative = 0
    
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
        red = (112, 31, 20)
        blue = (27, 97, 81)
        white = (163, 240, 147)
        black = (23, 34, 19)
        self.farbsensor.setColors(black, blue, red)
        self.motor.setOffset(self.farbsensor.convert(black), self.farbsensor.convert(white))
        time.sleep(1)
        print(f'Schwarz: {black}, Blau: {blue}, Rot: {red}, Weiß: {white}')

    def direction(self):
        alpha = 0
    
    def driving(self):
        print('Setzten Sie jetzt den Roboter an den gewünschten Punkt und drücken Sie eine Taste auf dem Roboter.')
        self.stealTime()
        loop = True
        # print(f'Start: Left: {self.leftMotor}, Right: {self.rightMotor} , Direction: {self.radians  * 360 / math.pi}')
        while loop:
            if self.ultrasonic.isSomethingInMyWay():
                print('something in my way')
                ev3.Sound.play('/home/robot/src/assets/quack.wav')
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
        # self.radians, self.pahts, self.colorArray[self.colorArray.__len__]
        return
    
    def turnAround(self):
        self.motor.curve(self.motor.ninety * 2)
        time.sleep(2.25)
        
    def driveAtPoint(self):
        self.motor.tare()
        self.motor.driveSevenCM()
        self.findPath()
        ev3.Sound.beep()
        self.totalDist = self.clacTotalDist()
        grad = self.radians * 180 / math.pi
        print(f'Der Roboter ist {self.roundToFifty(self.totalDist)}cm gefahren und damit {(self.roundToFifty(self.totalDist) / 50)} Kästchen')
        print(f'Der Roboter hat eine {self.roundToNinety(grad)}° Drehung gemacht')
        ev3.Sound.play('bark.wav')
    
    def driveLine(self, lightValue):
        temp = self.motor.driveLine(lightValue)
        self.getCurrentDist(temp[0], temp[1])
        
    def getCurrentDist(self, left, right):
        tempLeft = -self.calcDist(left + self.leftMotor['position'])
        tempRight = -self.calcDist(right + self.rightMotor['position'])
        self.leftMotor['position'] = -left
        self.rightMotor['position'] = -right
        self.calcDirection(tempLeft, tempRight)
    
    def calcDirection(self, left, right):
        self.radians += (right - left) / self.wheeldist
        
    def clacTotalDist(self):
        dr = self.calcDist(self.rightMotor['position'])
        dl = self.calcDist(self.leftMotor['position'])
        return self.wheeldist * ((dr + dl) / (dr - dl) * math.sin((dr - dl) / (2 * self.wheeldist)))
        
    def calcDist(self, degree):
        return degree * self.distPerDegree
    
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
