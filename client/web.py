from http.server import BaseHTTPRequestHandler, HTTPServer
import dht11

# HTTPRequestHandler class
class RequestHandler(BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        (humidity, temperature) = dht11.read_sensor_data()

        # Send message back to client
        message = "Temperature: {}C, humidity: {}%".format(temperature, humidity)
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('0.0.0.0', 8081)
    httpd = HTTPServer(server_address, RequestHandler)
    print('running server...')
    httpd.serve_forever()


run()