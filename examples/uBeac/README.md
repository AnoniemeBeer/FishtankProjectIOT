# uBeac connection

<img src="uBeacLogo.png">

uBeac is a free, easy to use online IOT platform

## Usage

To use the class, you first need to make an object with the class. The construction method takes one parameter: the https url of you uBeac gateway. This module is written to work with https requests.

This can be done the following way:

```python
uBeacSend = uBeac(url)
```

To update a sensor in uBeac, the following method should be used:
```python
uBeacSend.sendData(deviceName, sensorName, value)
```
This method takes three parameters. The first parameter is the name of your device in Ubeac, the second parameter is the name of the sensor you want to update. At last, the value you want to update the sensor to is given.

Its important to not spam the service, it will not work. After testing, half a second should be between two requests. If more is sent, it will not be recognized by the system. For bigger chuncks of data, there is another, more difficult method:

```python
uBeacSend.sendBigData(data)
```

This method requires one parameter. That parameter is a json with format:

```json
{
    "id": deviceName,
    "sensors": [
        {
            "id": sensorName1,
            "data": sensorValue1
        },
        {
            "id": sensorName2,
            "data": sensorValue2
        },
        {
            "id": sensorName3,
            "data": sensorValue3
        }
    ]
}
```

## Example script
```python
import requests
from random import randrange
import time

class uBeac:
    def __init__(self, url):
        self.url = url
    
    def sendData(self, deviceName, sensorName, sensorValue):
        data = {
            "id": deviceName,
            "sensors": [{
                "id": sensorName,
                "data": sensorValue
            }]
        }
        requests.post(self.url, json=data)

if __name__ == '__main__':
    url = "https://fishtank.hub.ubeac.io/main"
    uBeacSend = uBeac(url)
    while True:
        light = randrange(0, 101, 100)
        waterLevel = randrange(0, 20)
        pump = randrange(0, 101, 100)

        uBeacSend.sendData("raspberry pi", "waterLevel", waterLevel)
        time.sleep(0.5)
        uBeacSend.sendData("raspberry pi", "pump", pump)
        time.sleep(0.5)
        uBeacSend.sendData("raspberry pi", "light", light)
        time.sleep(0.5)
```