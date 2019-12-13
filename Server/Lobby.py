import Game
import threading
import time
import socket
import copy

#this is the lobby
class Lobby():
    #constor
    def __init__(self):
        self.__LobbyList = []
        self.__PeopleInGame = []

    #This will try to add a player to the lobby
    def connect(self, client, addr):
        if (self.__LobbyList.__len__() == 3):
            print("Error: lobby is full")
            return False
        self.__LobbyList.append((client, addr))
        print(str(addr) + " was added successfully")
        for x in self.__LobbyList:
            x[0].send("player joined the lobby!".encode())
        return True

    #this will remove a player from the lobby
    def remove(self, client, addr):
        self.__LobbyList.remove((client, addr))
        print(str(addr) + " was removed successfully")
        for x in self.__LobbyList:
            x[0].send("player disconnected from the lobby!".encode())

    #this check the lobby and see if player need to be moved to a game
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

    #this will check to see who is in a game
    def checkInGame(self, player):
        print("\n\npeople in games:")
        print(str(self.__PeopleInGame))
        for x in self.__PeopleInGame:
            if x == player:
                self.__PeopleInGame.remove(x)
                return True
        return False

    #this runs in a serprite thread and check the lobby and updates every 2 seconds
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