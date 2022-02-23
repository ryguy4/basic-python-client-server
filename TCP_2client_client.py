#############################################################################
# Program:
#   Lab TCP_2client_client, Computer Networking
#   Brother Jones, CSE 354
# Author:
#   Class supplied
# Summary:
#   This client is a CSE 354 Lab 1 supplied client to connect to an
#   enhanced TCP server that creates log files of all the messages
#   sent to it by two clients.
#
# Protocol description:
#   After a client does the TCP handshake and connection to the server,
#   The first message sent by each client is to provide the name of 
#   the file to be created by the server for this client. If the name
#   is accepted by the server, a reply message of FOK (filename ok)
#   will be returned by the server. If the file name is not accepted,
#   'ERROR' will be returned by the server and the server will expect
#   that the next message from the client is another try at giving a
#   valid file name. After a valid file name is given by a client and
#   the FOK message is received by the client, any further messages
#   sent by the client will be saved on the server system in the named
#   file until a single message that only consists of ".end" is sent.
#
#   If a file name of '.end' is sent by a client, the name is sent to
#   the server and everything shuts down.
#
#   The length of messages should be less than 1000 characters.
#
#   Status values returned by the server are:  FOK, OK and ERROR
#
#   Sample protocol diagram for a non-error session:
#       client1 <<--- TCP connection --->> server
#       client1 ------- file name ------>> server
#       client1 <<---------- FOK --------- server
#                           server <<--- TCP connection --->> client2
#                           server <<------ file name ------- client2
#                           server ---------- FOK --------->> client2
#       client1 -------- message ------->> server
#       client1 <<--------- OK ----------- server
#                           server <<------- message -------- client2
#                           server ---------- OK ---------->> client2
#       client1 -------- message ------->> server
#       client1 <<--------- OK ----------- server
#                           server <<------- message -------- client2
#                           server ---------- OK ---------->> client2
#                                    .
#                                    .
#                                    .
#       client1 --- '.end' message ----->> server
#                           server <<----- '.end' message --- client2
#                     TCP connections closed on both sides
#
#   There are various things to consider with the way the server and 
#   client have been defined. Things such as various error conditions
#   and if the server should quit, or restart looking for two more 
#   clients, when the clients it was working with want to stop. Another
#   more interesting item is if the client-server interaction could be
#   done such that a client is not blocked waiting for the other client
#   to connect and/or to send a message.  More to explore and learn!    
# 
#############################################################################

import sys
from socket import *

serverName = ''

# The following code uses sys.argv to handle command line arguments.
# You might want to learn about the argparse module.
#   https://docs.python.org/3/howto/argparse.html 
if len(sys.argv) < 3:
    print('Usage: TCP_2client_client hostname port')
    sys.exit(1)
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    # The 'message' variable is used in the loop that gets user input to
    # send to the server.  It is set to something other than '.end' here
    # so that if the user puts in '.end' instead of a file name, we 
    # terminate the program.
    message = 'something'

    fileNameStatus = 'ERROR'
    while (fileNameStatus != 'FOK'):
        userFileName = input(
            'Input the file name for the server to use to save messages: ')
        if (userFileName == '.end'):
            # User wants to terminate everything. Set the message variable
            # to '.end' and exit this loop. 
            message = userFileName
            break
        # Send the file name to the server
        clientSocket.send(userFileName.encode('ascii'))
        fileNameStatus = clientSocket.recv(1024).decode('ascii')
        if (fileNameStatus == 'FOK'):
            break
        # Might check for 'ERROR' from the server if the protocol was to
        # be extended with further capabilities.  For now, if we don't get
        # a 'FOK' we assume an 'ERROR' was sent.
        print('File name was not accepted by the server. Try again.')
    
    # Get messages from the user to save at the server until the user
    # inputs '.end'
    while (message != '.end'):
        # Get a message from the user and send it
        message = input('Input message to be saved at server: ')
        clientSocket.send(message.encode('ascii'))
        messageStatus = 'ERROR'
        print('Message sent to server. Waiting for status reply.')
        messageStatus = clientSocket.recv(1024).decode('ascii')
        if (messageStatus != 'OK'):
            # Something went wrong.  We could check for an 'ERROR' message,
            # but for now, this simple client will just shut down.
            # If it is a TCP level error, an exception would be thrown and
            # we will not be executing here anyway.
            print('Message status received from server: ', messageStatus)
            print('There was an error reported by the server; exiting program')
            clientSocket.close()
            sys.exit(2)
        print('Message status received from server: ', messageStatus)


    print('Terminating program on user request')
    # Tell the server we are done.  We will not wait for a status reply from the
    # server.  Should we?
    clientSocket.send('.end'.encode('ascii'))
    clientSocket.close()
    sys.exit(0)

# This client simply prints a message and exits when different errors occur.
# It does separate out a couple of errors giving additional information.
# Other errors in the ConnectionError class include: BrokenPipeError,
# ConnectionAbortedError, ConnectionRefusedError and ConnectionResetError
# that could be handled uniquely for each type of error.  
except KeyboardInterrupt:
    print('\nClosing Client')
    clientSocket.close()

except gaierror as e:
    print('Bad hostname: ', e)
    sys.exit(10)

except ConnectionRefusedError as e:
    # This is most likely, a bad port number
    print('Bad port number: ', e)

# The following could be used to figure out which type of exception occurred
# in order to put in specific error handling for it.  Thanks:
# https://stackoverflow.com/questions/19192891/how-to-handle-connectionerror-in-python
except Exception as e:
    print('Exception: ', type(e), type(e).__qualname__, e)
    sys.exit(11)




