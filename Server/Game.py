import Round

class Game():
    def __init__(self, players, gridSize, numOfRounds = 3):
        if (players.__len__() <= 1):
            raise ValueError("Error: Illegal state; number of players can not be less then 2")

        if (numOfRounds <= 0):
            raise ValueError("Error: Illegal state; number of Rounds can not be less then 1!")

        self.__players = players
        self.__gridSize = gridSize
        self.__numOfRound = numOfRounds - 1
        self.__scores = []
        self.__roundCurrent = None

        for x in players:
            temp = [x, 0]
            self.__scores.append(temp)

    def __getNextRoundLists(self, gameData):
        temp = []
        players = []
        colors = []

        for x in range(gameData.__len__() - 1, -1, -1):
            current = gameData.pop()
            players.append(current[0])
            colors.append(current[1])
            #print(str(players))
            #print(str(colors))
            self.__updateScore(current[0], x)
        
        temp.append(players)
        temp.append(colors)

        return temp

    def __updateScore(self, player, scoreChange):
        for x in self.__scores:
            if(x[0] == player):
                score = x.pop()
                score = score + scoreChange
                x.append(score)

    def __printScores(self):
        temp = []
        for x in self.__scores:
            copyFlip = [x[1], x[0]]
            temp.append(copyFlip)
            
        temp.sort()
        print("current Standings:")

        for x in range(0, temp.__len__()):
            current = temp.pop()
            print(str(x + 1) + ". " + str(self.__roundCurrent.getPlayerColor(current[1])) + " with " + str(current[0]) + " points!")

    def play(self):
        self.__roundCurrent = Round.Round(self.__players, self.__gridSize)
        gameData = self.__roundCurrent.run()

        gameLists = self.__getNextRoundLists(gameData)

        self.__printScores()

        input("press anything to continue...")

        for x in range(0, self.__numOfRound):
            self.__roundCurrent = Round.Round(gameLists[0], self.__gridSize, gameLists[1])
            gameData = self.__roundCurrent.run()

            gameLists = self.__getNextRoundLists(gameData)

            self.__printScores()
            input("press anything to continue...")
        