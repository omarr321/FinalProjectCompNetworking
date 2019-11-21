import Game
import threading
import time
import socket
import copy

class Lobby():
    def __init__(self):
        self.__LobbyList = []
        self.__PeopleInGame = []

    def connect(self, client, addr):
        if (self.__LobbyList.__len__() == 3):
            print("Error: lobby is full")
            return False
        self.__LobbyList.append((client, addr))
        print(str(addr) + " was added successfully")
        for x in self.__LobbyList:
            x[0].send("player joined the lobby!".encode())
        return True

    def remove(self, client, addr):
        self.__LobbyList.remove((client, addr))
        print(str(addr) + " was removed successfully")
        for x in self.__LobbyList:
            x[0].send("player disconnected from the lobby!".encode())

    def __checkLobby(self):
        print("checking Lobby...")
        print("\n\nlobby:")
        print("[", end = "")
        for x in self.__LobbyList:
            print(x[1], end = ", ")
        print("]")
        if(self.__LobbyList.__len__() == 3):
            print("Lobby is full; creating game...")
            return True
        return False

    def checkInGame(self, player):
        print("\n\npeople in games:")
        print(str(self.__PeopleInGame))
        for x in self.__PeopleInGame:
            if x == player:
                self.__PeopleInGame.remove(x)
                return True
        return False

    def run(self):
        while(True):
            if(self.__checkLobby()):
                for x in self.__LobbyList:
                    self.__PeopleInGame.append(x)
                newGame = Game.Game(self.__LobbyList, 5, 3)
                game = threading.Thread(target=newGame.play)
                game.start()
                self.__LobbyList = []
                print("Done!")
            else:
                print("Lobby still has room")
            time.sleep(2)