from turtle import forward
import RPi.GPIO as GPIO
import time

class fishFeederMotor:
    
    pins = []
    currentRotation = 0 # Rotation in steps
    stepSize = 36 # Step size in degrees
    stepSequence = [
        [False, True, True, True], 
        [False, False, True, True], 
        [True, False, True, True], 
        [True, False, False, True], 
        [True, True, False, True], 
        [True, True, False, False], 
        [True, True, True, False], 
        [False, True, True, False]
    ]
    stepSequenceStep = 0
    oneRevolution = 4076
    degreePerStep = 360 / oneRevolution

    def __init__(self, pinArray):
        self.pins = pinArray

    def setup(self):
        GPIO.setup(self.pins, GPIO.OUT)

    def setStepSize(self, stepSize):
        self.stepSize = stepSize

    def setFeederHoleAmount(self, amount):
        self.stepSize = 360 / amount

    def getCurrentRotation(self):
        return self.currentRotation

    def getCurrentDegrees(self):
        return self.currentRotation * self.degreePerStep

    def rotateOneStep(self, direction, step, stepsToRotate):

        if direction == "cw":
            GPIO.output(self.pins, self.stepSequence[step%8])

        elif direction == "ccw":
            GPIO.output(self.pins, self.stepSequence[stepsToRotate+1-(step%8)])


    def rotate(self, direction):

        stepsToRotate = int(self.stepSize // self.degreePerStep)
        
        if direction == "cw":
            for i in range(0, stepsToRotate):
                self.rotateOneStep("cw", i, stepsToRotate)
                time.sleep(0.002)

        if direction == "ccw":
            for i in range(0, stepsToRotate):
                self.rotateOneStep("ccw", i, stepsToRotate)
                time.sleep(0.002)

    def cleanUp(self):
        GPIO.output(pins, False)


if __name__ == "__main__":
    try:
        GPIO.setmode(GPIO.BCM)

        pins = [2, 3, 4, 17]
        stepperMotor = fishFeederMotor(pins)
        stepperMotor.setup()
        stepperMotor.setFeederHoleAmount(10)

        for i in range(0, 10):
            stepperMotor.rotate("ccw")


    except KeyboardInterrupt:
        stepperMotor.cleanUp()
        print("\nProgram stopped by user")
    stepperMotor.cleanUp()