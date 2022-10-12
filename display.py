""" MODULE USED TO MANAGE DISPLAYING GRID WITH BOT's CHARACTER """
import bext

class mazeHandler():
    
    def __init__(self, maze_fn, coords):

        self.maze_fn = maze_fn
        self.coords = coords 
        self.grid = None
        self.wall = chr(9619)
        self.bot = '@'

    def loadMaze(self):

        with open(self.maze_fn) as maze:
            self.grid = maze.readlines()
    
    def showMaze(self, clear=True):
        
        if clear:
            bext.clear()
        for row, line in enumerate(self.grid):
            for col, val in enumerate(line):
                if col == self.coords[0] and row == self.coords[1]:
                    print(self.bot, end='')
                elif val == '#':
                    print(self.wall, end='')
                elif val == 'E':
                    print('E', end='')
                else:
                    print(' ', end='')
            print()
    
    def getChar(self, coords):
        
        for row, line in enumerate(self.grid):
            for col, val in enumerate(line):
                if col == coords[0] and row == coords[1]:
                    return val

"""max_filename = "C:\\Users\\ernes\\Desktop\\Python PROJECTS\\MazeRunner\\maze.txt"

handler = mazeHandler(max_filename, (1, 1))
handler.loadMaze()
handler.showMaze()
handler.coords = (1, 4)
handler.showMaze()
print('ZNAK: ')
print(f'\'{handler.getChar((0, 0))}\'')"""