#############################################################################
# Program:
#   Lab TCP_2client_server, Computer Networking
#   Brother Jones, CSE 354
# Author:
#   Ryan Saunders
# Summary:
#   The purpose of this lab is to create a sever that allows for 2 TCP clients to connect to it. The clients will be able to
#   send a message to the server that will be saved in a file.
#
##############################################################################
# Note: Take-2 header goes here
#
##############################################################################

import sys
from socket import *

if len(sys.argv) < 2:
    print('Usage: TCP_2client_client hostname port')
    sys.exit(1)

serverPort = int(sys.argv[1])


serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
print('The Server is listening ... ')
print('Server waiting for two clients to connect ... ')

try:
    # Get connection to client 1
    connectionSocket1, addr1 = serverSocket.accept()
    # Open file received from client or return error if unable to open
    while True:
        try:
            fileName = connectionSocket1.recv(1024).decode('ascii')
            f1 = open(f"{fileName}", "a")
            print(f"File name received from client 1:  {fileName}")
            connectionSocket1.send("FOK".encode('ascii'))
            break                             
        except IOError:
            connectionSocket1.send("ERROR".encode('ascii'))

    # Get connection to client 2
    print('Server waiting for another client to connect ... ')
    connectionSocket2, addr2 = serverSocket.accept()

    # Open file received from client or return error if unable to open
    while True:
        try:
            fileName = connectionSocket2.recv(1024).decode('ascii')
            f2 = open(f"{fileName}", "a")
            print(f"File name received from client 2:  {fileName}")
            connectionSocket2.send("FOK".encode('ascii'))
            break                             
        except IOError:
            connectionSocket2.send("ERROR".encode('ascii'))

    c1Status = 1
    c2Status = 1
    while 1:
        # Check if client 1 has ended the connection yet. If it has not ended the connection, wait for a message and then add it to
        # the appropriate file.
        if c1Status:
            message = connectionSocket1.recv(1024).decode('ascii')
            if message == ".end":
                print(f"Message from client 2:  {message}")
                c1Status = 0
                connectionSocket1.send("OK".encode('ascii'))
            else:
                print(f"Message from client 1:  {message}")
                f1.write(message)
                f1.write("\n")
                connectionSocket1.send("OK".encode('ascii'))
        # Check if client 2 has ended the connection yet. If it has not ended the connection, wait for a message and then add it to
        # the appropriate file.
        if c2Status:
            message = connectionSocket2.recv(1024).decode('ascii')
            if message == ".end":
                print(f"Message from client 2:  {message}")
                c2Status = 0
                connectionSocket2.send("OK".encode('ascii'))
            else:
                print(f"Message from client 2:  {message}")
                f2.write(message)
                f2.write("\n")
                connectionSocket2.send("OK".encode('ascii'))

        # If both clients have ended either connection, then stop receiving messages
        if not c1Status and not c2Status:
            break

    # Close files and connections and stop the server.
    print("Server shutting down")
    print("Closing connections and exiting server")
    f1.close()
    connectionSocket1.close()
    f2.close()
    connectionSocket2.close()


except KeyboardInterrupt:
    print("\nClosing Server")
    serverSocket.close()