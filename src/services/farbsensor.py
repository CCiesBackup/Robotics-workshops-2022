#!/usr/bin/env python3
import ev3dev.ev3 as ev3
class Farbsensor:
    cs = ev3.ColorSensor()
    red = ()
    blue = ()
    yellow = ()
    black = ()
    
    def __init__(self):
        self.cs.mode = "RGB-RAW"
    
    def recognizeColour(self):
        red = self.cs.bin_data("hhh")[0]
        green = self.cs.bin_data("hhh")[1]
        blue = self.cs.bin_data("hhh")[2]
        if self.isBlue(red, green, blue):
            return 0
        elif self.isRed(red, green, blue):
            return 1
        elif self.isYellow(red, green, blue):
            return 2
        else:
            return self.getBlackWhitePortion(red, green, blue)
    
    def getBlackWhitePortion(self, red, green, blue):
        return (red + green + blue) / 765

    def isBlue(self, red, green, blue):
        if red <= (self.blue[0] + 10) and self.isBetween(green, self.blue[1]) and self.isBetween(blue, self.blue[2]) :
            print('Is blue!')
            return True
        return False
    
    def isRed(self, red, green, blue):
        if self.isBetween(red, self.red[0]) and green <= (self.red[1] + 20) and blue <= (self.red[2] + 20):
            print('Is red!')
            return True
        return False
    
    def isYellow(self, red, green, blue):
        if self.isBetween(red, self.yellow[0]) and self.isBetween(green, self.yellow[1])  and self.isBetween(blue, self.yellow[2]) :
            print('Is red!')
            return True
        return False
    
    def isBlack(self):
        red = self.cs.bin_data("hhh")[0]
        green = self.cs.bin_data("hhh")[1]
        blue = self.cs.bin_data("hhh")[2]
        if red <= (self.black[0] + 20) and green <= (self.black[1] + 20) and blue <= (self.black[2] + 20):
            return True
        return False
    
    def getRawColor(self):
        return self.cs.bin_data("hhh")
    
    def setColors(self, black, blue, red, yellow):
        self.black = black
        self.blue = blue
        self.red = red
        self.yellow = yellow
        
    def convert(self, tupel):
        return (tupel[0] + tupel[1] + tupel[2]) / 765
    
    def isBetween(self, new, color):
        if new >= (color - 20) and new <= (color + 20):
            return True
        return False
