from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime, timedelta
from threading import currentThread

from modules.relay import relay

import RPi.GPIO as GPIO

hostName = "localhost"
serverPort = 12345

status = 0

GPIO.setmode(GPIO.BCM)

light = relay(26)

turnOff = 0
currentDatetime = datetime.now()
turnOffDatetime = currentDatetime.replace(microsecond=0)

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        global turnOff, currentDatetime, turnOffDatetime
        currentDatetime = datetime.now()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path == "/light/switchOn":
            status = 1
            light.setStatus(status)
            turnOffDatetime = currentDatetime.replace(microsecond=0) + timedelta(minutes=15)
            turnOff = 1

            print(turnOff)
            print(turnOffDatetime)
            print(currentDatetime)
        
        if self.path == "/light/switchOff":
            status = 0
            light.setStatus(status)
            turnOff = 0
        
        if self.path == "/light/switchStatus":
            print(turnOff)
            if turnOff == 1:
                print(turnOffDatetime)
                print(currentDatetime)
                if currentDatetime > turnOffDatetime:
                    turnOff = 0
                    status = 0
                    light.setStatus(status)
                    print("Turn off")

            status = light.getStatus()
            self.wfile.write(bytes(str(status), "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")