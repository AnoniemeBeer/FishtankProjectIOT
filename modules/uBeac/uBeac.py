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

    def sendBigData(self, data):
        requests.post(self.url, json=data)


if __name__ == '__main__':
    url = "https://fishtank.hub.ubeac.io/main"
    uBeacSend = uBeac(url)
    delay = 0.5
    while True:
        uBeacSend.sendData("raspberry pi", "waterLevel", 20)
        time.sleep(delay)
        uBeacSend.sendData("raspberry pi", "pump", 100)
        time.sleep(delay)
        uBeacSend.sendData("raspberry pi", "light", 100)
        time.sleep(delay)
        uBeacSend.sendData("raspberry pi", "waterLevel", 0)
        time.sleep(delay)
        uBeacSend.sendData("raspberry pi", "pump", 0)
        time.sleep(delay)
        uBeacSend.sendData("raspberry pi", "light", 0)
        time.sleep(delay)