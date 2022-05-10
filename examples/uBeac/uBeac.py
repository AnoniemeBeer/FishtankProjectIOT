import requests
from random import randrange
import time

class uBeac:
    # constructor, takes the url of the uBeac server
    def __init__(self, url):
        self.url = url
    
    # send data to uBeac, takes the devicename to upload to, 
    def sendData(self, deviceName, sensorName, sensorValue):
        data = {
            "id": deviceName,
            "sensors": [{
                "id": sensorName,
                "data": sensorValue
            }]
        }
        requests.post(self.url, json=data)

    # send data to uBeac, the array that is generated automatically in the method above has to be provided by the user via the parameter
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