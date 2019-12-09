#!/usr/bin/env python
from beautifultable import BeautifulTable
import json
import socket
import time

class Grid:
    def __init__(self):
        self.table = BeautifulTable()
    def create(self, size):
        row = [' '] * size
        for i in range(0, 5):
            self.table.append_row(row)

    def getTable(self):
        return self.table

    def set(self, x, y, color):
        self.table[y][x] = color

def __charPrint(string, endChar = "\n", timePerChar = .04):
    for x in string:
        print(x, end="", flush=True)
        time.sleep(timePerChar)
    print("", end=endChar)

def __clearScreen():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('10.220.82.180', 255))

grid = Grid()
grid.create(5)

myColor = ''

__charPrint('Waiting', endChar="")

while True:
    data = socket.recv(1024)
    data = data.decode()

    if data.rstrip('\n') == 'alive?':
        socket.send('yes'.encode())
        __charPrint(".", endChar="")

    elif data.rstrip('\n') == 'game start':
        print("")
        __charPrint('Starting Game!')

    try:
        jsonData = json.loads(data)
        if 'board' in jsonData:
            board = json.loads(jsonData['board'])

            __clearScreen()

            for jsonObject in board:
                for color, value in jsonObject.items():
                    for coords in value['ownedTiles']:
                        x = coords[0] - 1
                        y = coords[1] - 1
                        if coords == value['currentTile']: color = '( %s )' % color
                        grid.set(x, y, color)

            temp = str(grid.getTable())
            temp = temp.split("\n")

            for x in temp:
                print(x)
                time.sleep(.1)

            #print(grid.getTable()

        if 'yourColor' in jsonData:
            myColor = jsonData['yourColor']

        if jsonData['request'] is True and jsonData['type'] == 'move':

            __charPrint("Your move " + str(myColor) + " (UP, DOWN, LEFT, RIGHT):")
            __charPrint(">>>", endChar="")
            move = input("")

            socket.send(json.dumps({'move': move}).encode())
    except ValueError as e:
        pass

   # if not data: break

socket.close()
