import time
import RPi.GPIO as GPIO

class relay:
    pin = 0
    status = True
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, True)
    
    def setStatus(self, status):
        self.status = status
        GPIO.output(self.pin, self.status)
    
    def toggleStatus(self):
        self.status = not self.status
        GPIO.output(self.pin, self.status)

    def cleanUp(self):
        GPIO.output(self.pin, True)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    light = relay(26)

    light.setup()

    try:
        while True:
            light.toggleStatus()
            time.sleep(1)
    except KeyboardInterrupt:
        light.cleanUp()