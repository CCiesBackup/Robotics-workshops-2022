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
    
    def __init__(self):
        """
        Initializes odometry module
        """

    def direction(self):
        alpha = 0
    
    def linefollowing(self):
        left = ev3.LargeMotor("outA")
        right = ev3.LargeMotor("outD")
        
        left.reset()
        right.reset()
        
        left.stop_action = "brake"
        right.stop_action = "brake"
        
        left.command = "run-forever"
        right.command = "run-forever"
        
        kp = 300
        offset = 0.5
        cs = ev3.ColorSensor()
        cs.mode = "COL-COLOR"
        cs.mode = "RGB-RAW"
        while True:
            print(cs.bin_data("hhh"))
            LightValue = self.farbsensor.getBlackWhitePortion(cs.bin_data("hhh")[0], cs.bin_data("hhh")[1], cs.bin_data("hhh")[2])
            error = LightValue - offset
            print(f'Error: {error}')
            self.strategy.driving(error * kp, left, right)
