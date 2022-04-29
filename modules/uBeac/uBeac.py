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
        response = requests.post(self.url, json=data)
        return response.text

if __name__ == '__main__':
    url = "https://fishtank.hub.ubeac.io/main"
    uBeacSend = uBeac(url)
    while True:
        light = randrange(0, 101, 100)
        waterLevel = randrange(0, 20)
        pump = randrange(0, 101, 100)

        uBeacSend.sendData("raspberry pi", "waterLevel", waterLevel)
        uBeacSend.sendData("raspberry pi", "pump", pump)
        uBeacSend.sendData("raspberry pi", "light", light)
        time.sleep(1)