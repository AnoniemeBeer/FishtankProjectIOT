import requests

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