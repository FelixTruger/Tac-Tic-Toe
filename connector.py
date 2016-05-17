import socket
import sys

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ep = None # endpoint when started as server

def startServer(port):
    global connection
    global ep

    try:
        connection.bind(("", port))
        connection.listen(1)
        print("Server is started and listening on port " + str(port) + ".")
        (clientsocket, address) = connection.accept()
        ep = clientsocket
        print("Client has connected.")
        return 1
    except socket.error as msg:
        connection.close()
        connection = None

    if connection is None:
        print("Could not open socket")
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialize new socket
        return 0

def startClient(ip, port):
    global connection
    try:
        connection.connect((ip, port))
        print("Client is started and connected to IP: " + str(ip) + " on port: " + str(port) + ".")
        return 1
    except socket.error as msg:
        connection.close()
        connection = None

    if connection is None:
        print("Could not open socket")
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialize new socket
        return 0

def send(message):
    if connection is None:
        return 0
    
    message = str(message)
    if ep:
        ep.send(message.encode())
    else:
        connection.send(message.encode())
    #print("Sent message: "+message)
    return 1

def receive():
    if connection is None:
        return 0
    #print("Waiting for message...")
    if ep:
        message = ep.recv(1024).decode()
    else:
        message = connection.recv(1024).decode()
    #print("Received message: "+message)
    return message
  
def close():
    global ep
    global connection
    
    if ep is not None:
        ep.close()
        ep = None
        connection.shutdown(socket.SHUT_RDWR)
    if connection is not None:
        connection.close()
        
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # initialize new socket
    
    print("Connection closed.")

if __name__ == '__main__':
    print("Tac-Tic-Toe Connector module Copyright (C) 2016  Felix & Hagen\n\
    This program comes with ABSOLUTELY NO WARRANTY; for details see GPL.\n\
    This is free software, and you are welcome to redistribute it\n\
    under certain conditions; see GPL for details.")
    print()
    print(">>>>>This module has no functionality on its own!<<<<<")
    print("Run main.py or use this module in another python script by importing it.")