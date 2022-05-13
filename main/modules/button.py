import RPi.GPIO as GPIO

class button:
    # constructor for the button, takes the pin number as an argument
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # setup the interrupt for the button, takes the function to be called as an argument
    def setupInterrupt(self, interruptFunction):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=interruptFunction, bouncetime=30)

    # cleanup the GPIO pins
    def cleanup(self):
        GPIO.cleanup()