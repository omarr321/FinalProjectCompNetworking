import GameBoard
import copy

class Round():
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

    def __movePlayer(self, player, xChange, yChange):
        try:
            self.__gameBoard.movePlayer(player, xChange, yChange)
            return True
        except ValueError as ve:
            print(ve)
            return False
    
    def __getInput(self, player):
        while(True):
            valueIn = input(">")
            if(self.__checkInput(valueIn)):
                return valueIn
            print("Error: not vaild input; try again:")

    def __checkInput(self, input):
        vaildIn = False

        if (input == "UP" or input == "DOWN" or input == "LEFT" or input == "RIGHT"):
            vaildIn = True
        
        return vaildIn

    def __checkPlayer(self, player):
        return not(self.__gameBoard.canMove(player))

    def __printGame(self):
        data = self.__gameBoard.getPlayersTiles()

        for y in range(1, self.__gridSize + 1):
            for p in range(1, self.__gridSize):
                print("-----", end = "", flush = True)
            print("------")
            for x in range(1, self.__gridSize + 1):
                dataPrintFlag = False
                for d in data:
                    
                    for t in d[2]:
                        
                        if (t == [x, y]):
                            if (d[0] == "Red"):
                                if (d[1] == t):
                                    print("|(re)", end = "", flush = True)
                                else:
                                    print("| re ", end = "", flush = True)
                                dataPrintFlag = True
                            elif (d[0] == "Blue"):
                                if (d[1] == t):
                                    print("|(bl)", end = "", flush = True)
                                else:
                                    print("| bl ", end = "", flush = True)
                                dataPrintFlag = True
                            elif (d[0] == "Green"):
                                if (d[1] == t):
                                    print("|(gr)", end = "", flush = True)
                                else:
                                    print("| gr ", end = "", flush = True)
                                dataPrintFlag = True
                            elif (d[0] == "Purple"):
                                if (d[1] == t):
                                    print("|(pu)", end = "", flush = True)
                                else:
                                    print("| pu ", end = "", flush = True)
                                dataPrintFlag = True
                            elif (d[0] == "Pink"):
                                if (d[1] == t):
                                    print("|(pi)", end = "", flush = True)
                                else:
                                    print("| pi ", end = "", flush = True)
                                dataPrintFlag = True
                if (not(dataPrintFlag)):
                    print("|    ", end = "", flush = True)
            print("|")
        for p in range(1, self.__gridSize):
            print("-----", end = "", flush = True)
        print("------")

    def getPlayerColor(self, player):
        return self.__gameBoard.getPlayerColor(player)

    def run(self):
        while (self.__currentPlayers.__len__() > 1):
            for x in self.__currentPlayers:

                print ("Current Turn: " + self.__gameBoard.getPlayerColor(x))
                
                self.__printGame()
                print("What would you like to do? (UP, DOWN, LEFT, RIGHT)")
                while(True):
                    moveIn = self.__getInput(x)
                    if(moveIn == "RIGHT"):
                        if(self.__movePlayer(x, 1, 0)):
                            break
                        print("Try again")
                    elif(moveIn == "LEFT"):
                        if(self.__movePlayer(x, -1, 0)):
                            break
                        print("Try again")
                    elif(moveIn == "UP"):
                        if(self.__movePlayer(x, 0, -1)):
                            break
                        print("Try again")
                    elif(moveIn == "DOWN"):
                        if(self.__movePlayer(x, 0, 1)):
                            break
                        print("Try again")

                for x in self.__currentPlayers:
                    if (self.__checkPlayer(x)):
                        self.__currentPlayers.remove(x)
                        temp = [x, self.__gameBoard.getPlayerColor(x)]
                        self.__listInWiningOrder.append(temp)
        temp = [self.__currentPlayers[0], self.__gameBoard.getPlayerColor(self.__currentPlayers[0])]
        self.__listInWiningOrder.append(temp)
        self.__printGame()
        print(self.__gameBoard.getPlayerColor(self.__currentPlayers[0]) + " has won the round!")
        input("press anything to continue...")
        return copy.deepcopy(self.__listInWiningOrder)

        