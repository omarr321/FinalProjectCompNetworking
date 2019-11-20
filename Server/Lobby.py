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
        if (self.__LobbyList.__len__() == 2):
            print("Error: lobby is full")
            return False
        self.__LobbyList.append((client, addr))
        print(str(addr) + " was added successfully")
        return True

    def remove(self, client, addr):
        self.__LobbyList.remove((client, addr))
        print(str(addr) + " was removed successfully")

    def __checkLobby(self):
        print("checking Lobby...")
        print("[", end = "")
        for x in self.__LobbyList:
            print(x[1], end = ", ")
        print("]")
        if(self.__LobbyList.__len__() == 2):
            print("Lobby is full; creating game...")
            return True
        return False

    def startGame(self):
        print("starting game...")
        gameList = self.__LobbyList
        time.sleep(5)
        temp = Game.Game(gameList, 5, 3)
        # temp.play()
        print("reached the end")

    def run(self):
        while(True):
            if(self.__checkLobby()):
                newGame = Game.Game(self.__LobbyList, 5, 3)
                game = threading.Thread(target=newGame.play)
                game.start()
                self.__LobbyList = []
                print("Done!")
            else:
                print("Lobby still has room")
            time.sleep(2)