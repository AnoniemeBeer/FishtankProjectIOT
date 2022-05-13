import RPi.GPIO as GPIO

class relay:
    status = 1
    manual = 0

    # Constructor, takes a pin number that is connected to the relay
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, 1)
    
    # setter, sets the status of the relay and turns it on or off
    def setStatus(self, status):
        if status == 0:
            self.status = 1
        elif status == 1:
            self.status = 0
        GPIO.output(self.pin, self.status)
    
    # toggle the status of the relay and turns it on or off
    def toggleStatus(self):
        if self.status == 0:
            self.status = 1
        elif self.status == 1:
            self.status = 0
        GPIO.output(self.pin, self.status)

    # getter, returns the status of the relay
    def getStatus(self):
        self.status = GPIO.input(self.pin)
        if self.status == False:
            return 1
        else:
            return 0

    # setter, sets the manual status of the relay which is used by the phone controller
    def setManual(self, status):
        self.manual = status

    # getter, returns the manual status of the relay
    def getManual(self):
        return self.manual

    def cleanUp(self):
        GPIO.output(self.pin, True)