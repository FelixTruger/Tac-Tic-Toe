import socket
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def startServer(port):
    global server

    try:
        server.bind(("", port))
        server.listen(1)
        print("Server is started and listening on port " + str(port) + ".")
    except socket.error as msg:
        server.close()
        server = None

    if server is None:
        print("could not open socket")
        sys.exit(1)

def startClient(ip, port):
    global client
    try:
        client.connect((ip, port))
        print("Client is started and connected to IP: " + str(ip) + " on port: " + str(port) + ".")
    except socket.error as msg:
        client.close()
        client = None

    if client is None:
        print("could not open socket")
        sys.exit(1)


