import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta

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

        # -----------------------------------------------------------------------------------------------------------------
        # *All global variables are defined here
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

        #setting all variables used by the feeder
        feederHoleAmount = 10

        # -----------------------------------------------------------------------------------------------------------------
        # *All objects are made here
        # making objects for the different modules
        feedCwButton = button(feedCwButtonPin)
        feedCcwButton = button(feedCcwButtonPin)
        lightButton = button(lightButtonPin)
        pumpButton = button(pumpButtonPin)
        
        feeder = fishFeederMotor(feederPins)

        lcdScreen = lcdScreen()
        lcdScreen.setImage('../images/fish.png')

        light = relay(lightRelayPin)
        pump = relay(pumpRelayPin)

        uBeac = uBeac(uBeacUrl)

        ultrasonicSensor = ultrasonicSensor(triggerPin, echoPin)

        # setting up the feeder
        feeder.setFeederHoleAmount(feederHoleAmount)

        # -----------------------------------------------------------------------------------------------------------------
        # *user choices are made here

        normalWaterdistance = 10        # the distance that the water should be at at least
        timeForFeeding = "15:00:00"     # the time that the feeder should rotate every day (format: hh:mm:ss)
        timeForLightOn = "22:00:00"     # the time that the light should be turned on every day(format: hh:mm:ss)
        timeForLightOff = "06:00:00"    # the time that the light should be turned off every day(format: hh:mm:ss)

        # -----------------------------------------------------------------------------------------------------------------
        # *defining all variables
        # time variables
        currentDatetime = datetime.now()
        ultrasonicTime = datetime.now().replace(microsecond=0)

        feederTime = datetime.now().replace(hour=datetime.strptime(timeForFeeding, "%H:%M:%S").hour, minute=datetime.strptime(timeForFeeding, "%H:%M:%S").minute, second=datetime.strptime(timeForFeeding, "%H:%M:%S").second, microsecond=0)
        if feederTime.time() < currentDatetime.time():
            feederTime = feederTime + timedelta(days=1)

        lightOnTime = datetime.now().replace(hour=datetime.strptime(timeForLightOn, "%H:%M:%S").hour, minute=datetime.strptime(timeForLightOn, "%H:%M:%S").minute, second=datetime.strptime(timeForLightOn, "%H:%M:%S").second, microsecond=0)
        if lightOnTime.time() < currentDatetime.time():
            lightOnTime = lightOnTime + timedelta(days=1)
        lightOffTime = datetime.now().replace(hour=datetime.strptime(timeForLightOff, "%H:%M:%S").hour, minute=datetime.strptime(timeForLightOff, "%H:%M:%S").minute, second=datetime.strptime(timeForLightOff, "%H:%M:%S").second, microsecond=0)
        if lightOffTime.time() < currentDatetime.time():
            lightOffTime = lightOffTime + timedelta(days=1)

        lcdTime = datetime.now().replace(microsecond=0)

        # lcd variables

        lcdTextArray = ["", "", "", "", ""]
        oldLcdTextArray = ["", "", "", "", ""]

        # ultrasonic sensor variables
        waterdistance = 0
        previousWaterdistance = 0

        # button variables
        manualPump = 0

        # -----------------------------------------------------------------------------------------------------------------
        # *Button functions
        # creating the button functions
        def feedCw(channel):
            feeder.rotate("cw")

        def feedCcw(channel):
            feeder.rotate("ccw")

        def lightToggle(channel):
            light.toggleStatus()
            print("Setting the light status: ", light.getStatus())
            uBeac.sendData("raspberry pi", "light", light.getStatus()*100)

        def pumpToggle(channel):
            pump.toggleStatus()
            print("Setting the pump status: ", pump.getStatus())
            pump.setManual(1)
            uBeac.sendData("raspberry pi", "pump", pump.getStatus()*100)

        # making the button interrupts
        feedCwButton.setupInterrupt(feedCw)
        feedCcwButton.setupInterrupt(feedCcw)
        lightButton.setupInterrupt(lightToggle)
        pumpButton.setupInterrupt(pumpToggle)

        # -----------------------------------------------------------------------------------------------------------------
        # *Setup, mainly generating the first LCD screen (runs once)
        # giving time to the ultrasonic sensor to calibrate
        lcdTextArray[0] = str(currentDatetime.strftime("%H:%M:%S"))
        time.sleep(2)
        waterdistance = ultrasonicSensor.getDistance()
        lcdTextArray[1] = "Water: " + str(waterdistance)
        lcdTextArray[2] = str(timedelta(seconds=int((feederTime - currentDatetime).total_seconds())))

        if light.getStatus() == 1:
            lcdTextArray[3] = "Light: On"
            lcdTextArray[4] = str(timedelta(seconds=int((lightOffTime - currentDatetime).total_seconds())))

        elif light.getStatus() == 0:
            lcdTextArray[3] = "Light: Off"
            lcdTextArray[4] = str(timedelta(seconds=int((lightOnTime - currentDatetime).total_seconds())))
        
        lcdScreen.clearDisplay()
        lcdScreen.setText(lcdTextArray)
        oldLcdTextArray = list(lcdTextArray)

        # checking if light should be on or off
        if timedelta(seconds=int((lightOffTime - currentDatetime).total_seconds())) < timedelta(seconds=int((lightOnTime - currentDatetime).total_seconds())):
            light.setStatus(1)
            uBeac.sendData("raspberry pi", "light", light.getStatus()*100)
        # -----------------------------------------------------------------------------------------------------------------
        # *Main loop
        # the main loop (runs forever)
        while True:
            # updating the current time variable
            currentDatetime = datetime.now()


            # reading the ultrasonic sensor and dealing with anything it has to deal with
            
            if ultrasonicTime < currentDatetime:
                waterdistance = ultrasonicSensor.getDistance()
                print("Water distance:", waterdistance, "cm")

                # if the water level changed by more than 1 cm
                if waterdistance - 1 > previousWaterdistance or waterdistance + 1 < previousWaterdistance:
                    lcdTextArray[1] = "Water: " + str(waterdistance)
                    previousWaterdistance = waterdistance

                    uBeac.sendData("raspberry pi", "waterLevel", int(waterdistance))

                ultrasonicTime = ultrasonicTime + timedelta(seconds=1)

                if waterdistance > float(normalWaterdistance):
                    if pump.getStatus() == 0 and pump.getManual() == 0:
                        pump.setStatus(1)
                        print("Pump turned on")
                        uBeac.sendData("raspberry pi", "pump", pump.getStatus()*100)
                    
                if waterdistance < float(normalWaterdistance):
                    if pump.getStatus() == 1 and pump.getManual() == 0:
                        pump.setStatus(0)
                        print("Pump turned off")
                        uBeac.sendData("raspberry pi", "pump", pump.getStatus()*100)

            # rotating feeder at the correct time
            if feederTime < currentDatetime:
                feeder.rotate("cw")
                feederTime = feederTime + timedelta(days=1)
                print("Feeding the fish")

            # turning the light on and off at the correct time

            if lightOnTime < currentDatetime:
                light.setStatus(1)
                uBeac.sendData("raspberry pi", "light", light.getStatus()*100)
                lightOnTime = lightOnTime + timedelta(days=1)
                print("Turning on the light")

            if lightOffTime < currentDatetime:
                light.setStatus(0)
                uBeac.sendData("raspberry pi", "light", light.getStatus()*100)
                lightOffTime = lightOffTime + timedelta(days=1)
                print("Turning off the light")

            # updating the lcd screen when there is a change to the data

            if lcdTime < currentDatetime:
                lcdTextArray[0] = str(currentDatetime.strftime("%H:%M:%S"))
                lcdTime = lcdTime + timedelta(seconds=1)

                lcdTextArray[2] = str(timedelta(seconds=int((feederTime - currentDatetime).total_seconds())))

                if light.getStatus() == 1:
                    lcdTextArray[3] = "Light: On"
                    lcdTextArray[4] = str(timedelta(seconds=int((lightOffTime - currentDatetime).total_seconds())))

                elif light.getStatus() == 0:
                    lcdTextArray[3] = "Light: Off"
                    lcdTextArray[4] = str(timedelta(seconds=int((lightOnTime - currentDatetime).total_seconds())))


                # print the current time
                print(currentDatetime.strftime("%H:%M:%S"))

            # at the end of the main loop, the lcd screen is updated if the text has changed
            if lcdTextArray!= oldLcdTextArray:
                lcdScreen.setText(lcdTextArray)
                oldLcdTextArray = list(lcdTextArray)

    except KeyboardInterrupt:
        # cleanup functions to be called when the program is interrupted by the user

        feeder.cleanUp()
        lcdScreen.clearDisplay()
        light.cleanUp()
        pump.cleanUp()
        ultrasonicSensor.cleanup()
        

        print("\nProgram stopped by user")