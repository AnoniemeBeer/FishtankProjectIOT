import requests
from random import randrange
import time

class uBeac:
    pass

if __name__ == '__main__':
    while True:
        light = randrange(0, 101, 100)
        waterLevel = randrange(0, 20)
        pump = randrange(0, 101, 100)

        url = "https://fishtank.hub.ubeac.io/main"
        data = {
                    "id": "Jules",
                    "sensors":[{
                        "id": "light",
                        "data": light
                    },
                    {
                        "id": "waterLevel",
                        "data": waterLevel
                    },
                    {
                        "id": "pump",
                        "data": pump
                    }]
                }
        response = requests.request("POST", url, json=data)
        print(response.text)
        time.sleep(1)
