import copy

#this class host the player and all player data
class Player():
    #constructor
    def __init__(self, posX, posY, color, gridSize, clientInfo):
        if(posX > gridSize or posX <= 0):
            raise ValueError("Error: illegal state; Player must start within the grid!")

        if(posX > gridSize or posX <= 0):
            raise ValueError("Error: illegal state; Player must start within the grid!")

        self.__currentPos = [posX, posY]
        self.__color = color
        self.__tiles = []
        self.__gridSize = gridSize
        self.__clientInfo = clientInfo

        self.__addTile(posX, posY)

    #this will add a tile to the tiles that this player owns
    def __addTile(self, posX, posY):
        self.__tiles.append([posX, posY])

    #This will check the move and makes sure it vaild and will raise an exseption if not
    def __checkMove(self, xPos, xChange, yPos, yChange):
        if (xChange > 1 or xChange < -1):
            raise ValueError("Error:illegal move; Player can not move more then one tile at a time!")

        if (yChange > 1 or yChange < -1):
            raise ValueError("Error:illegal move; Player can not move more then one tile at a time!")

        if (xChange + yChange == 0):
            raise ValueError("Error:illeagl move; Player did not move!")

        if (xChange != 0 and yChange != 0):
            raise ValueError("Error:illeagl move; Player can not move diagonally!")

        if (yPos + yChange > self.__gridSize or yPos + yChange <= 0):
            raise ValueError("Error:illegal move; Player can not move outside the grid!")

        if (xPos + xChange > self.__gridSize or xPos + xChange <= 0):
            raise ValueError("Error:illegal move; Player can not move outside the grid!")

    #this will move the player
    def move(self, xChange, yChange):
        self.__checkMove(self.__currentPos[0], xChange, self.__currentPos[1], yChange)

        self.__currentPos[0] = self.__currentPos[0] + xChange
        self.__currentPos[1] = self.__currentPos[1] + yChange
        
        self.__addTile(self.__currentPos[0], self.__currentPos[1])

    #this gets the tile list
    def getTiles(self):
        return copy.deepcopy(self.__tiles)
        #return self.__tiles

    #this gets the current postion
    def getCurrentPos(self):
        return copy.deepcopy(self.__currentPos)
        #return self.__currentPos

    #this gets the color
    def getColor(self):
        return copy.deepcopy(self.__color)
        #return self.__color

    #This gets the info of the client connection
    def getClientInfo(self):
        return copy.copy(self.__clientInfo)
        #return self.__clientInfo

    #this returns a string of all data
    #---used for debugging mostly
    def toString(self):
        return "Player addr: " + str(self.__clientInfo) + "\nPlayer color: " + str(self.__color) + "\nPlayer current position: " + str(self.__currentPos) + "\nTiles owned: " + str(self.__tiles)