from turtle import forward
import RPi.GPIO as GPIO
import time

class fishFeederMotor:
    
    pins = []
    currentRotation = 0 # Rotation in steps
    stepSize = 36 # Step size in degrees
    # stepSequence = [[0, 1, 1, 1], [0, 0, 1, 1], [1, 0, 1, 1], [1, 0, 0, 1], [1, 1, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0], [0, 1, 1, 0]]
    stepSequence = [[False, True, True, True], [False, False, True, True], [True, False, True, True], [True, False, False, True], [True, True, False, True], [True, True, False, False], [True, True, True, False], [False, True, True, False]]
    stepSequenceStep = 0
    degreePerStep = 360 / 4096

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

    def rotateOneStep(self, direction):
        GPIO.output(self.pins, self.stepSequence[self.stepSequenceStep])

        self.stepSequenceStep = self.stepSequenceStep + direction
        if self.stepSequenceStep == 7:
            self.stepSequenceStep = 0
        if self.stepSequenceStep == -1:
            self.stepSequenceStep = 7

    def rotate(self, steps):
        
        if steps == "cw":
            stepsToRotate = self.stepSize // self.degreePerStep
            for i in range(0, int(stepsToRotate)):
                self.rotateOneStep(1)
                time.sleep(0.003)
                self.currentRotation = self.currentRotation + 1
        if steps == "ccw":
            stepsToRotate = self.stepSize // self.degreePerStep
            for i in range(0, int(stepsToRotate)):
                self.rotateOneStep(-1)
                time.sleep(0.003)
                self.currentRotation = self.currentRotation - 1
            

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
            stepperMotor.rotate("cw")

    except KeyboardInterrupt:
        stepperMotor.cleanUp()
        print("\nProgram stopped by user")
    stepperMotor.cleanUp()