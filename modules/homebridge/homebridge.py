from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 12345

status = 0


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        if self.path == "/light/switchOn":
            print("Switch On")
            status = 1
        
        if self.path == "/light/switchOff":
            print("Switch Off")
            status = 0
        
        if self.path == "/light/getStatus":
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