# Lcd Screen

This class is written for a blue NoKia 5110 lcd screen. This lcd screen needs five input pins, as well as 3.3V and GND. In the schema's down below, the connections are shown. The needed connections are:

<table>
    <tr>
        <th>LCD</th>
        <th>Pin number</th>        
        <th>RPI</th>
        <th>Pin number</th>
    </tr>
    <tr>
        <td>Reset</td>
        <td>1</td>
        <td>GPIO24</td>
        <td>18</td>
    </tr>    
    <tr>
        <td>Chip Enable</td>
        <td>2</td>
        <td>CE1</td>
        <td>26</td>
    </tr>
    <tr>
        <td>Data/Command</td>
        <td>3</td>
        <td>GPIO23</td>
        <td>16</td>
    </tr>
    <tr>
        <td>Data In</td>
        <td>4</td>
        <td>Mosi</td>
        <td>19</td>
    </tr>
    <tr>
        <td>Clock</td>
        <td>5</td>
        <td>SCLK</td>
        <td>23</td>
    </tr>
    <tr>
        <td>VCC</td>
        <td>6</td>
        <td>3.3V</td>
        <td>1</td>
    </tr>
    <tr>
        <td>Backlight</td>
        <td>7</td>
        <td>3.3V</td>
        <td>1</td>
    </tr>    
    <tr>
        <td>Ground</td>
        <td>8</td>
        <td>Ground</td>
        <td>6</td>
    </tr>
</table>

<img src="fritzing.png" height="400px"> <img src="schema.png" height="400px">

## Usage


To use the class, you first need to make an object with the class. The construction method takes one parameter: the GPIO pin number that the relay is connected to.
This can be done  the following way:

```python
objectName = lcdScreen()
```

If the object is made, you can start to use the methods of the class. To set the state of the relay pin, the following method is used.

```python
objectName.setText(text)
```

Aside from setting the state, there is also a way to toggle it:

```python
objectName.clearDisplay()
```

## Example script
```python
import time
import RPi.GPIO as GPIO
class ultrasoneSensor:
    
    def __init__(self, triggerPin, echoPin):
        self.trig = triggerPin
        self.echo = echoPin
    
    def setup(self):
        GPIO.setup(self.trig, GPIO.OUT)
        GPIO.setup(self.echo, GPIO.IN)

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
        
    def cleanup(self):
        GPIO.output(self.trig, False)
        GPIO.cleanup()


if __name__ == '__main__':

    GPIO.setmode(GPIO.BCM)

    sensor = ultrasoneSensor(13, 6)
    sensor.setup()

    while True:
        distance = sensor.getDistance()
        print(distance)
        time.sleep(1)
```