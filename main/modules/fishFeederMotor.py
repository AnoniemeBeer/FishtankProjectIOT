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

    # Constructor, takes an array of pins that are connected to the motor
    def __init__(self, pinArray):
        self.pins = pinArray
        GPIO.setup(self.pins, GPIO.OUT)

    # setter, sets the step size of the motor
    def setStepSize(self, stepSize):
        self.stepSize = stepSize
    
    # setter, sets the amount of holes in the feeder
    # calculates the stepsize based on the amount of holes
    def setFeederHoleAmount(self, amount):
        self.stepSize = 360 / amount

    # rotates the motor one step, takes a direction and a step
    def rotateOneStep(self, direction, step):

        if direction == "cw":
            GPIO.output(self.pins, self.stepSequence[step%8])

        elif direction == "ccw":
            GPIO.output(self.pins, self.stepSequence[7-(step%8)])

    # rotates the motor to the next hole
    def rotate(self, direction):

        stepsToRotate = int(self.stepSize // self.degreePerStep)
        
        if direction == "cw":
            for i in range(0, stepsToRotate):
                self.rotateOneStep("cw", i)
                time.sleep(0.002)

        if direction == "ccw":
            for i in range(0, stepsToRotate):
                self.rotateOneStep("ccw", i)
                time.sleep(0.002)

    # cleans up the pins, sets all the pins of the motor to false, so the motor's coils are not energized
    def cleanUp(self):
        GPIO.output(self.pins, False)