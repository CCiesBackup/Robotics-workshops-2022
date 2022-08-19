#!/usr/bin/env python3

import ev3dev.ev3 as ev3

class Motor(object):
    tp = 150
    
    def __init__(self):
        """
        Initializes odometry module
        """
        
class LeftEdge(Motor):
    
    def __init__():
        super().__init__()
    
    def driving(powerLevel, left, right):
        tp = 150   
        powerA = tp - powerLevel
        powerD = tp + powerLevel
        
        left.speed_sp = -(powerA)
        right.speed_sp = -(powerD)
        
        left.command = "run-forever"
        right.command = "run-forever"
        return

class RightEdge(Motor):

    def __init__():
        super().__init__()
    
    def driving(powerLevel, left, right):
        tp = 150
        powerA = tp + powerLevel
        powerD = tp - powerLevel
        
        left.speed_sp = -(powerA)
        right.speed_sp = -(powerD)
        
        left.command = "run-forever"
        right.command = "run-forever"
        return