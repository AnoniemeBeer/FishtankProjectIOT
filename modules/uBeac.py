import requests
from random import randrange

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