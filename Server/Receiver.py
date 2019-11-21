import socket
import threading
import time
import Lobby

#Edit these host and port to change where the server runs on; leave host blank if you want it to run on local host
HOST = "10.220.82.180"
PORT = 255
lobby = Lobby.Lobby()

class Receiver():
    def __init__(self, host, port, lobby):
        self.host = host
        self.port = port
        self.lobby = lobby
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((self.host, self.port))
        newLobby = threading.Thread(target=lobby.run)
        newLobby.start()
        print("The server is ready to receive...")
    
    def listen(self):
        self.serverSocket.listen(3)
        while(True):
            client, addr = self.serverSocket.accept()
            newThread = threading.Thread(target = self.ClientController,args = (client, addr))
            newThread.start()


    def ClientController(self, client, addr):
        closed = False
        try:
            lobbyTry = 0
            while(True):
                print(str(addr) + " is trying to connect to lobby...")
                if (self.lobby.connect(client, addr) == True):
                    print(str(addr) + " is connected to the lobby!")
                    break

                if (lobbyTry == 2):
                    int("well... shit")
                lobbyTry = lobbyTry + 1
                time.sleep(1)
        except ValueError as ve:
            print(str(addr) + " tried connected three times and failed")
            print("closing connection...")
            client.send("500 can not connect to server".encode())
            client.close()
            closed = True
            print("Done!")
        except:
            print(client + " has disconnected!")
            print("Cleaning up...")
            client.close()
            closed = True
            print("Done!")

        if (closed == False):
            try:
                client.send("200 ok".encode())
                
                time.sleep(1)

                while(True):
                    if (self.lobby.checkInGame((client, addr)) == True):
                        print(str(addr) + " is in a game exiting Receiver...")
                        client.send("game start".encode())
                        break
                    else:
                        client.send("alive?".encode())
                        client.recv(1024)
                    time.sleep(1)
            except:
                print(str(addr) + " has disconnected!")
                print("Cleaning up...")
                self.lobby.remove(client, addr)
                client.close()
                print("Done!")

temp = Receiver(HOST, PORT, lobby)
temp.listen()