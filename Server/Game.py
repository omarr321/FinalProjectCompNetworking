import Round
import time
import json
import socket

#this runs the game
class Game():
    #this is a construor
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

    #this will return the the list of players and list of colors in winning order
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

    #This will update the score
    def __updateScore(self, player, scoreChange):
        for x in self.__scores:
            if(x[0] == player):
                score = x.pop()
                score = score + scoreChange
                x.append(score)

    #This will send scores the the players in the game
    def __sendScores(self, final):
        temp = []
        for x in self.__scores:
            copyFlip = [x[1], x[0]]
            temp.append(copyFlip)

        temp.sort()
        
        pythonData = []
        for x in range(0, temp.__len__()):
            pythonData.append(temp.pop())
        jsonData = json.dumps(pythonData)

        if (final == False):
            data = {
            "request":False,
            "type":"ScoreBoard",
            "scores":jsonData
            }
        else:
            data = {
            "request":False,
            "type":"FinalScoreBoard",
            "scores":jsonData
            }
        data = json.dumps(data)

        for x in self.__players:
            x[0].send(data.encode())        

    #This will play the game
    def play(self):
        time.sleep(5)
        self.__roundCurrent = Round.Round(self.__players, self.__gridSize)
        gameData = self.__roundCurrent.run()

        gameLists = self.__getNextRoundLists(gameData)

        print("sending scores...")
        self.__sendScores(False)

        print("continuing after 5 seconds...")
        time.sleep(5)

        for x in range(0, self.__numOfRound):
            self.__roundCurrent = Round.Round(gameLists[0], self.__gridSize, gameLists[1])
            gameData = self.__roundCurrent.run()

            gameLists = self.__getNextRoundLists(gameData)

            if (x == self.__numOfRound):
                print("sending final scores...")
                self.__sendScores(True)
            else:
                print("sending scores...")
                self.__sendScores(False)
            
            print("continuing after 5 seconds...")
            time.sleep(5)
        
        print("ending game...")
        print("Done!")