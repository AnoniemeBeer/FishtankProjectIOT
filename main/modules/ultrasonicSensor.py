import time
import RPi.GPIO as GPIO

class ultrasonicSensor:
    # constructor, initialize the sensor
    def __init__(self, triggerPin, echoPin):
        self.trig = triggerPin
        self.echo = echoPin
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

    # getter, return the distance
    def getDistance(self):
            GPIO.output(self.trig, True)
            time.sleep(0.00001)
            GPIO.output(self.trig, False)

            while GPIO.input(self.echo)==0:
                pulse_start = time.time()

            while GPIO.input(self.echo)==1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration * 17150
            distance = round(distance, 2)

            return distance
        
    # cleanup function, clean up the GPIO
    def cleanup(self):
        GPIO.output(self.trig, False)
        GPIO.cleanup()