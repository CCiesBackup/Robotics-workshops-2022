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
from services.motor import LeftEdge


class Odometry:
    colorArray = []
    strategy = LeftEdge
    farbsensor = Farbsensor
    left = ev3.LargeMotor("outA")
    right = ev3.LargeMotor("outD")
    kp = 300
    offset = 0.5
    cs = ev3.ColorSensor()
    
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
    
    def linefollowing(self):
        print(self.cs.bin_data("hhh"))
        LightValue = self.farbsensor.getBlackWhitePortion(self.cs.bin_data("hhh")[0], self.cs.bin_data("hhh")[1], self.cs.bin_data("hhh")[2])
        error = LightValue - self.offset
        print(f'Error: {error}')
        self.strategy.driving(error * self.kp, self.left, self.right)
