from random import choice
import bext, os
import time
from datetime import datetime
from display import mazeHandler as mh

"""
AUTHOR: Ernest Morawski
VERSION: ALPHA
"""

maze_filename = "C:\\Users\\ernes\\Desktop\\Python PROJECTS\\MazeRunner\\maze2.txt" #Make it relevant to your directory

class Bot():

    def __init__(self):
        
        self.position = (1,1) # x, y
        self.map = []

        self.handler = mh(maze_filename, self.position)
        self.handler.loadMaze()
        
        self.updateBlocksAround()

        self.mapMarks = 0

        self.foundExit = False

    def showLogs(self):

        for i in self.map:
            for k, v in i.items():
                print(f'{k}: {v}')
            print('----------')
    
    def updateBlocksAround(self):

        self.left  = (self.position[0] - 1, self.position[1])
        self.right = (self.position[0] + 1, self.position[1])
        self.up    = (self.position[0], self.position[1] - 1)
        self.down  = (self.position[0], self.position[1] + 1)

    def isPossible(self, coords):
        
        char = self.handler.getChar(coords)
        if char == ' ':
            return True
        else:
            return False
    
    def prevDirection(self):
        
        try:
            lastChosenWay = self.map[-1]['chosenWays'][-1]
            if lastChosenWay == 'down':
                return 'up'
            if lastChosenWay == 'up':
                return 'down'
            if lastChosenWay == 'left':
                return 'right'
            if lastChosenWay == 'right':
                return 'left'

        except IndexError:
            return 'brak'
    
    def deleteLastTreeInMap(self, index):

        indexOfLastCrossing = index + 1
        
        while len(self.map) != indexOfLastCrossing:
            del self.map[-1]

        self.mapMarks = indexOfLastCrossing + 1     

    def goToLastCrossing(self):
        ways = []

        while True:

            waysThatWasChosenInLastCrossing = []
            possibleWaysOfLastCrossing = []

            indexOfLastCrossing = None

            coordsOfCrossing = (0, 0)

            for count, item in enumerate(self.map):
                if item['isCrossing'] == True:
                    indexOfLastCrossing = count
                    possibleWaysOfLastCrossing = item['possibleWays'][:]
                    waysThatWasChosenInLastCrossing = item['chosenWays'][:]
                    coordsOfCrossing = (item['bot_x'], item['bot_y'])
            
        
            for way in possibleWaysOfLastCrossing:
                if way not in waysThatWasChosenInLastCrossing:
                    ways.append(way)

            if len(ways) > 0:
                self.position = coordsOfCrossing
                self.handler.coords = self.position
                newWay = choice(ways)
                self.map[indexOfLastCrossing]['chosenWays'].append(newWay)
                self.deleteLastTreeInMap(indexOfLastCrossing)
                return newWay
                break
            else:
                del self.map[indexOfLastCrossing]

    def addMapElement(self):

        foundSimilarElm = False
        for elm in self.map:
            if elm['bot_x'] == self.position[0] and elm['bot_y'] == self.position[1]:
                foundSimilarElm = True

        if not foundSimilarElm:

            mapElement = {
                'bot_x': self.position[0],
                'bot_y': self.position[1],
                'possibleWays': self.getPossibleWays(),
                'wayBack': self.prevDirection(),
                'isCrossing': False,
                'index': self.mapMarks,
                'chosenWays': [],
            }

            self.map.append(mapElement)
            self.mapMarks = self.mapMarks + 1

    def getPossibleWays(self, *deadEnds):

        possibleWays = []
        self.updateBlocksAround() # updating self.left, self.right etc...

        if self.isPossible(self.left) and 'left' not in deadEnds:
            possibleWays.append('left')
        if self.isPossible(self.right) and 'right' not in deadEnds:
            possibleWays.append('right')
        if self.isPossible(self.up) and 'up' not in deadEnds:
            possibleWays.append('up')
        if self.isPossible(self.down) and 'down' not in deadEnds:
            possibleWays.append('down')

        try: #Try to delete way we come at certain place from out of possible ways
            wayBack = self.prevDirection()
            wayBack = possibleWays.index(wayBack)

        except ValueError:
            pass
        else:
            del possibleWays[wayBack]

        return possibleWays

    def whichWay(self):

        ways = self.map[-1]['possibleWays']
        if len(ways) > 0:
            chosenWay = choice(ways)
            self.map[-1]['chosenWays'].append(chosenWay)
        else:
            chosenWay = self.goToLastCrossing()
            #print(f'I GOT CHOSEN WAY FROM LAST CROSSING: {chosenWay}') - LOG INFO
            #print(f'and pos x {self.position[0]} and {self.position[1]}')
        if len(ways) > 1:
            self.map[-1]['isCrossing'] = True

        return chosenWay

    def isExitFound(self):
        
        if self.handler.getChar(self.position) == 'E':
            self.foundExit = True

    def go(self):
        
        chosenWay = self.whichWay()

        if self.handler.getChar(self.position) != 'E':
            self.updateBlocksAround()
            if chosenWay == 'down':
                while self.handler.getChar(self.down) != '#':
                    self.position = (self.position[0], self.position[1] + 1)
                    self.updateBlocksAround()
                    if self.handler.getChar(self.right) == ' ':
                        break
                    if self.handler.getChar(self.left) == ' ':
                        break

            elif chosenWay == 'up':
                while self.handler.getChar(self.up) != '#':
                    self.position = (self.position[0], self.position[1] - 1)
                    self.updateBlocksAround()
                    if self.handler.getChar(self.right) == ' ':
                        break
                    if self.handler.getChar(self.left) == ' ':
                        break

            elif chosenWay == 'right':
                while self.handler.getChar(self.right) != '#':
                    self.position = (self.position[0] + 1, self.position[1])
                    self.updateBlocksAround()
                    if self.handler.getChar(self.up) == ' ':
                        break
                    if self.handler.getChar(self.down) == ' ':
                        break

            elif chosenWay == 'left':
                while self.handler.getChar(self.left) != '#':
                    self.position = (self.position[0] - 1, self.position[1])
                    self.updateBlocksAround()
                    if self.handler.getChar(self.up) == ' ':
                        break
                    if self.handler.getChar(self.down) == ' ':
                        break

            self.handler.coords = self.position
        else:
            self.foundExit = True

    def mainLoop(self):

        self.start = datetime.now()
        while self.foundExit == False:
            
            self.handler.showMaze()
            self.addMapElement()
            self.go()
            self.isExitFound()
            time.sleep(0.2)      
        #self.showLogs()
        self.handler.showMaze()
        print('YEAH I FINALLY FOUND AN EXIT')
        self.end = datetime.now()
        result = self.end - self.start
        print(f"time: {result}")
        

bot = Bot()
bot.mainLoop()
