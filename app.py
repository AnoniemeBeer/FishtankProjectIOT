import RPi.GPIO as GPIO
import time
import busio
import digitalio
import board
import adafruit_pcd8544
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import requests

from modules.button import button
from modules.fishFeederMotor import fishFeederMotor
from modules.lcdScreen import lcdScreen
from modules.relay import relay
from modules.uBeac import uBeac
from modules.ultrasonicSensor import ultrasonicSensor

if __name__ == "__main__":
    try:
        # determine the type of gpio notation we are using
        GPIO.setmode(GPIO.BCM)

        #setting up the variables that store the gpio pins
        feedCwButtonPin = 21
        feedCcwButtonPin = 20
        lightButtonPin = 16
        pumpButtonPin = 12

        feederPins = [2, 3, 4, 17]

        lightRelayPin = 26
        pumpRelayPin = 19

        uBeacUrl = "https://fishtank.hub.ubeac.io/main"

        triggerPin = 13
        echoPin = 6


        # makind objects for the different modules
        feedCwButton = button(feedCwButtonPin)
        feedCcwButton = button(feedCcwButtonPin)
        lightButton = button(lightButtonPin)
        pumpButton = button(pumpButtonPin)

        feeder = fishFeederMotor(feederPins)

        lcdScreen = lcdScreen()

        light = relay(lightRelayPin)
        pump = relay(pumpRelayPin)

        uBeac = uBeac(uBeacUrl)

        ultrasonicSensor = ultrasonicSensor(triggerPin, echoPin)

        # Creating the button functions

        

    except KeyboardInterrupt:
        #cleanup functions to be called
        print("\nProgram stopped by user")