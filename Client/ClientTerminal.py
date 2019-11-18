from socket import *

HOST = "10.220.82.180"
PORT = 255
server = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(server)
while(True):
    print("Connected...")

#----------Code example----------
#----not used in final design----
#from socket import *
#
#HOST = "10.220.90.5"
#serverPort = 25535
#
#message = input("Input lowercase sentence:")
#
#clientSocket = socket(AF_INET, SOCK_STREAM)
#clientSocket.connect((HOST, serverPort))
#clientSocket.sendto(message.encode(), (HOST, serverPort))
#modifiedMessage = clientSocket.recv(1024)
#print(modifiedMessage.decode())
#clientSocket.close()