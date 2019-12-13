import Player
import copy

playerClass = Player.Player;
import random

#is the game board whitch is a grid of player and tiles
class GameBoard():
    #construtor
    def __init__(self, gridSize = 10):
        
        if (gridSize <= 0):
            raise ValueError("Error: illegal state; gridSize must be positive!")
        self.__gridSize = gridSize
        self.__playerList = []
        self.__colors = ["Red", "Green", "Blue", "Pink", "Purple"]

    #this will check to see if a postion is free to move on to
    def __isFree(self, posX, posY):
        for player in self.__playerList:
            for tile in player.getTiles():
                if (tile == [posX, posY]):
                    return False

        if((posX > self.__gridSize or posX <= 0) or (posY > self.__gridSize or posY <= 0)):
            return False

        return True    

    #this will add a player to the game board
    def addPlayer(self, player, color = None):
        if(color != None):
            placed = False;
            while (not(placed)):
                xPos = random.randint(1, self.__gridSize)
                yPos = random.randint(1, self.__gridSize)

                if (self.__colors.__len__() == 0):
                    raise LookupError("Error: Illegal LookUp; There are no more unique colors left to assign!")

                if (self.__isFree(xPos, yPos)):
                    self.__playerList.append(playerClass(xPos, yPos, color, self.__gridSize, player))
                    self.__colors.remove(color)
                    placed = True  
        else:
            self.__addPlayerNoColor(player)  

    #this also adds a player to the game board but will no random colors
    def __addPlayerNoColor(self, player):
        placed = False;
        while (not(placed)):
            xPos = random.randint(1, self.__gridSize)
            yPos = random.randint(1, self.__gridSize)

            if (self.__colors.__len__() == 0):
                raise LookupError("Error: Illegal LookUp; There are no more unique colors left to assign!")

            color = random.randint(0, self.__colors.__len__() - 1)

            if (self.__isFree(xPos, yPos)):
                self.__playerList.append(playerClass(xPos, yPos, self.__colors[color], self.__gridSize, player))
                self.__colors.remove(self.__colors[color])
                placed = True   

    #this will move a player and check to see if it vaild
    def movePlayer(self, player, xChange, yChange):
        for x in self.__playerList:
            if (x.getClientInfo() == player):
                if (self.__isFree(x.getCurrentPos()[0] + xChange, x.getCurrentPos()[1] + yChange)):
                    x.move(xChange, yChange)
                else:
                    raise ValueError("Error: Illegal move")

    #this will check to see if the player can move
    def canMove(self, player):
        canMoveFlag = False

        for x in self.__playerList:
            if (x.getClientInfo() == player):
                currentPos = x.getCurrentPos()

                for xp in (-1, 0, 1):
                    for yp in (-1, 0, 1):

                        if (not(xp + yp == 0) and not(xp != 0 and yp != 0)):
                            xPos = currentPos[0] + xp
                            yPos = currentPos[1] + yp
                            if(self.__isFree(xPos, yPos)):
                                canMoveFlag = True;
        
        return canMoveFlag    

    #this returns the data to a string
    def toString(self):
        temp = ""
        for x in self.__playerList:
            temp = temp + x.toString() + "\n\n"

        return temp

    #this gets all the tiles that all players own
    def getPlayersTiles(self):
        data = []
        #{"red": {"currentTile": [0, 0], "ownedTiles": [[0, 0], [0, 1]]}}
        for x in self.__playerList:
            data.append({x.getColor(): {'currentTile': x.getCurrentPos(), 'ownedTiles': x.getTiles()}})
           # data.append([x.getColor(), x.getCurrentPos(), x.getTiles()])
        
        return data

    #this reuturns a player color
    def getPlayerColor(self, player):
        for x in self.__playerList:
            if (x.getClientInfo() == player):
                return str(x.getColor())
        
        return ""
