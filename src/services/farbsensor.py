import ev3dev.ev3 as ev3
class Farbsensor:
    cs = ev3.ColorSensor()
    
    def __init__(self):
        self.cs.mode = "RGB-RAW"
    
    def recognizeColour(self):
        if self.isBlue():
            return 0
        elif self.isBlue():
            return 1
        else:
            return self.getBlackWhitePortion()
    
    def getBlackWhitePortion(self):
        red = self.cs.bin_data("hhh")[0]
        green = self.cs.bin_data("hhh")[1]
        blue = self.cs.bin_data("hhh")[2]
        return (red + green + blue) / 765

    def isBlue(self):
        red = self.cs.bin_data("hhh")[0]
        green = self.cs.bin_data("hhh")[1]
        blue = self.cs.bin_data("hhh")[2]
        if red <= 35 and green >= 70 and green <= 105 and blue >= 75 and blue <= 90:
            print('Is blue!')
            return True
        return False
    
    def isRed(self):
        red = self.cs.bin_data("hhh")[0]
        green = self.cs.bin_data("hhh")[1]
        blue = self.cs.bin_data("hhh")[2]
        if red >= 100 and red <= 200 and green <= 70 and blue <= 70:
            print('Is red!')
            return True
        return False
    
    def isBlack(self):
        red = self.cs.bin_data("hhh")[0]
        green = self.cs.bin_data("hhh")[1]
        blue = self.cs.bin_data("hhh")[2]
        if red <= 100 and green <= 100 and blue <= 100:
            print('Is black!')
            return True
        return False
