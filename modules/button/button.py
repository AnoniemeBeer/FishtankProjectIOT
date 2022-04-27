import RPi.GPIO as GPIO
import time
import signal
import sys

class button:
    def __init__(self, pin):
        self.pin = pin

    def setup(self):
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def setupInterrupt(self, interruptFunction):
        GPIO.add_event_detect(self.pin, GPIO.FALLING, callback=interruptFunction, bouncetime=30)


def buttonFunction(channel):
    print("Button pressed!  ", end="")
    print(time.strftime("%H:%M:%S"))
    print(channel)

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    button1 = button(21)
    button1.setup()
    button1.setupInterrupt(buttonFunction)

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()