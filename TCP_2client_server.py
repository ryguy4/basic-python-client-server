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
# Changes made to my code for the Lab 1 Take-2:
# - Reduced code redundancy by putting repeated code into a function.
# - Slightly modified/corrected comments throughout the code to futher clarify what is happening and make things easier to read.
#
##############################################################################

import sys
from socket import *


def openFile(connection, clientNum):
    """
    Get a file name from the provided connection and try to open the file. Returns the open file once succesfully opened.
    """
    while 1:
        try:
            fileName = connection.recv(1024).decode('ascii')
            file = open(f"{fileName}", "a")
            print(f"File name received from client {clientNum}:  {fileName}")
            connection.send("FOK".encode('ascii'))
            return file                             
        except IOError:
            connection.send("ERROR".encode('ascii'))

def receiveWriteMessage(connection, clientNum, file):
    """
    Gets a message from the server and writes it to the provided file unless the message is ".end". Returns 1 if a normal message was received, 0 if signal to close connection was received.
    """
    message = connection.recv(1024).decode('ascii')
    print(f"Message from client {clientNum}:  {message}")
    if message == ".end":
        connection.send("OK".encode('ascii'))
        return 0
    else:
        file.write(message)
        file.write("\n")
        connection.send("OK".encode('ascii'))
        return 1

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
    # Get connection to client 1 then open the file received from the client or return an error is unable to open
    connectionSocket1, addr1 = serverSocket.accept()
    f1 = openFile(connectionSocket1, 1)

    # Get connection to client 2 then open the file received from the client or return an error is unable to open
    print('Server waiting for another client to connect ... ')
    connectionSocket2, addr2 = serverSocket.accept()
    f2 = openFile(connectionSocket2, 2)

    c1Status = 1
    c2Status = 1
    while 1:
        # Check if a client has ended the connection yet. If it has not ended the connection, wait for a message and then add it to the appropriate file.
        if c1Status:
            c1Status = receiveWriteMessage(connectionSocket1, 1, f1)
        if c2Status:
            c2Status = receiveWriteMessage(connectionSocket2, 2, f2)

        # If both clients have ended their connection, then stop receiving messages
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
