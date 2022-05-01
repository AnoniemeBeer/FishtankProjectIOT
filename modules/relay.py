import RPi.GPIO as GPIO

class relay:
    status = 1
    manual = 0
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 1)
    
    def setStatus(self, status):
        if status == 0:
            self.status = 1
        elif status == 1:
            self.status = 0
        GPIO.output(self.pin, self.status)
    
    def toggleStatus(self):
        if self.status == 0:
            self.status = 1
        elif self.status == 1:
            self.status = 0
        GPIO.output(self.pin, self.status)

    def getStatus(self):
        self.status = GPIO.input(self.pin)
        if self.status == False:
            return 1
        else:
            return 0

    def setManual(self, status):
        self.manual = status

    def getManual(self):
        return self.manual

    def cleanUp(self):
        GPIO.output(self.pin, True)