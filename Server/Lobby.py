from socket import *

HOST = "10.220.82.180"
PORT = 255
server = (HOST, PORT)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(server)
serverSocket.listen(10)
print("The server is ready to receive...")

while(True):
    gameList = []
    while(gameList.__len__() < 3):
        connectSocket, addr = serverSocket.accept()
        gameList.append(addr)
        print(str(gameList))
    print("That is three people")
    print(str(gameList))
    break

#----------Code example----------
#----not used in final design----
#from socket import *
#
#HOST = '10.220.90.5'
#serverPort = 25535
#
#serverSocket = socket(AF_INET, SOCK_STREAM)
#serverSocket.bind((HOST, serverPort))
#serverSocket.listen(1)
#print('The server is ready to receive')
#while True:
#    connectionSocket, addr = serverSocket.accept()
#
#    message = connectionSocket.recv(1024).decode()
#    print('message recieved:', message)
#    modifiedMessage = message.upper()
#    print('message edited:', modifiedMessage)
#    connectionSocket.send(modifiedMessage.encode())
#    print('Message has been sent back')
#
#    connectionSocket.close()