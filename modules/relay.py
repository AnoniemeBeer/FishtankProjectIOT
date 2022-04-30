import RPi.GPIO as GPIO

class relay:
    pin = 0
    status = True
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, True)
    
    def setStatus(self, status):
        self.status = not status
        GPIO.output(self.pin, self.status)
    
    def toggleStatus(self):
        self.status = not self.status
        GPIO.output(self.pin, self.status)

    def cleanUp(self):
        GPIO.output(self.pin, True)