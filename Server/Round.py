import GameBoard
import copy
import time
import json
import socket


#This is the Round class
#This class runs one round of the game

class Round():
    #Constructor for players, gridSize, and optional color
    def __init__(self, players, gridSize, colors = None):
        if (colors != None):
            self.__players = players
            self.__gridSize = gridSize
            self.__currentPlayers = players
            self.__listInWiningOrder = []
            try:
                self.__gameBoard = GameBoard.GameBoard(self.__gridSize)
            except ValueError as ve:
                print(ve)

            for x in range(0, players.__len__()):
                try:
                    self.__gameBoard.addPlayer(players[x], colors[x])
                except LookupError as le:
                    print(le)
        else:
            self.__noColor(players, gridSize)

    #This is called when the colors of the construster is set to none
    #this set up just like the construce just with random given numbers
    def __noColor(self, players, gridSize):
        self.__players = players
        self.__gridSize = gridSize
        self.__currentPlayers = players
        self.__listInWiningOrder = []
        try:
            self.__gameBoard = GameBoard.GameBoard(self.__gridSize)
        except ValueError as ve:
            print(ve)

        for x in players:
            try:
                self.__gameBoard.addPlayer(x)
            except LookupError as le:
                print(le)

    #this method will try to move the player by the x and y change. Will return true if sussful, false if not.
    def __movePlayer(self, player, xChange, yChange):
        try:
            self.__gameBoard.movePlayer(player, xChange, yChange)
            return True
        except ValueError as ve:
            print(ve)
            return False
    
    #this will get input from the current turn player and send back if the move was bad other will continue
    def __getInput(self, player, badMove = False):
        while(True):
            if (badMove == False):
                data = {
                    "request":True,
                    "type":"move"
                }
            else:
                data = {
                    "request":True,
                    "type":"move",
                    "error":"Not a vaild input or format"
                }
            data = json.dumps(data)
            data = '%s%s' % (data, '\n')
            player[0].send(data.encode())
            badMove = False
            data = player[0].recv(1024).decode()
            try:
                data = json.loads(data)
                valueIn = data["move"]
                if(self.__checkInput(valueIn)):
                    return valueIn
                print("Error: not vaild input")
                badMove = True
            except:
                print("Error: not vaild format")
                badMove = True
                

    #this checks the input of the player and sees if it a vaild format/move
    def __checkInput(self, input):
        vaildIn = False

        if (input == "UP" or input == "DOWN" or input == "LEFT" or input == "RIGHT"):
            vaildIn = True
        
        return vaildIn

    #This will checkt to see if a player can move or not
    def __checkPlayer(self, player):
        return not(self.__gameBoard.canMove(player))

    #This will send the game to a player
    def __sendGame(self, currentPlayer, request, yourColor = None):
        pythonData = self.__gameBoard.getPlayersTiles()
        pythonData = json.dumps(pythonData)
        color = json.dumps(self.__gameBoard.getPlayerColor(currentPlayer))

        if (yourColor == None):
            data = {
                "request":request,
                "type":"gameBoard",
                "currentPlayer":color,
                "board":pythonData
            }
        else:
            data = {
                "request":request,
                "type":"gameBoardFirst",
                "yourColor":yourColor,
                "currentPlayer":color,
                "board":pythonData
            }
        jsonData = json.dumps(data)
        print(jsonData)
        jsonData = '%s%s' % (jsonData, '\n')
        currentPlayer[0].send(jsonData.encode())
        
        
    #This get a player color
    def getPlayerColor(self, player):
        return self.__gameBoard.getPlayerColor(player)

    #This is what runs the round and will return the scoreboard of the game total
    def run(self):
        for x in self.__players:
            self.__sendGame(x, False, self.__gameBoard.getPlayerColor(x))

        while (self.__currentPlayers.__len__() > 1):
            for x in self.__currentPlayers:

                print ("Current Turn: " + self.__gameBoard.getPlayerColor(x))
                flag = False
                while(True):
                    if (flag == False):
                        moveIn = self.__getInput(x)
                    else:
                        moveIn = self.__getInput(x, True)
                    flag = False
                    if(moveIn == "RIGHT"):
                        if(self.__movePlayer(x, 1, 0)):
                            break
                        flag = True
                    elif(moveIn == "LEFT"):
                        if(self.__movePlayer(x, -1, 0)):
                            break
                        flag = True
                    elif(moveIn == "UP"):
                        if(self.__movePlayer(x, 0, -1)):
                            break
                        flag = True
                    elif(moveIn == "DOWN"):
                        if(self.__movePlayer(x, 0, 1)):
                            break
                        flag = True

                for x in self.__players:
                    self.__sendGame(x, False)

                for x in self.__currentPlayers:
                    if (self.__checkPlayer(x)):
                        self.__currentPlayers.remove(x)
                        temp = [x, self.__gameBoard.getPlayerColor(x)]
                        self.__listInWiningOrder.append(temp)
        temp = [self.__currentPlayers[0], self.__gameBoard.getPlayerColor(self.__currentPlayers[0])]
        self.__listInWiningOrder.append(temp)
        print(self.__gameBoard.getPlayerColor(self.__currentPlayers[0]) + " has won the round!")
        print("continuing after 5 seconds...")
        time.sleep(5)
        return copy.copy(self.__listInWiningOrder)

        