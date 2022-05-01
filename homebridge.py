from http.server import BaseHTTPRequestHandler, HTTPServer

from modules.relay import relay

import RPi.GPIO as GPIO

hostName = "localhost"
serverPort = 12345

status = 0

GPIO.setmode(GPIO.BCM)

light = relay(26)

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path == "/light/switchOn":
            status = 1
            light.setStatus(status)
        
        if self.path == "/light/switchOff":
            status = 0
            light.setStatus(status)
        
        if self.path == "/light/switchStatus":
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