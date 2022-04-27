import RPi.GPIO as GPIO

class relay:
    pin = 0
    def __init__(self, pin):
        self.pin = pin
    
    def setup(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def setupInterrupt(self): 
        pass

    

if __name__ == "__main__":
    pass