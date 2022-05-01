import RPi.GPIO as GPIO

class button:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def setupInterrupt(self, interruptFunction):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=interruptFunction, bouncetime=30)

    def cleanup(self):
        GPIO.cleanup()