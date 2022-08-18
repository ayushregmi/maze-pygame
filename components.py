import pygame
import math
# from main import ROW, COLUMN, ROW_WIDTH, COLUMN_WIDTH, ROW_GAP, COLUMN_GAP, TOP_GAP, BOTTOM_GAP, LEFT_GAP, RIGHT_GAP

# defining number, size and width of nodes
ROW = 20
COLUMN = 40
ROW_WIDTH = 20
COLUMN_WIDTH = 20
ROW_GAP = 2
COLUMN_GAP = 2
TOP_GAP = 1
BOTTOM_GAP = 1
LEFT_GAP = 1
RIGHT_GAP = 1
SCREEN_HEIGHT = ROW * ROW_WIDTH + (ROW + 1) * ROW_GAP + LEFT_GAP * 2
SCREEN_WIDTH = COLUMN * COLUMN_WIDTH + (COLUMN + 1) * COLUMN_GAP + TOP_GAP * 2
DIRECTIONSX = [0, 1, 0, -1]
DIRECTIONSY = [1, 0, -1, 0]   

#defining the nodes as class
class Node:
    def __init__(self, i, j):
        self.i = i
        self.j = j
        self.x = i * ROW_WIDTH + (i + 1) * ROW_GAP + LEFT_GAP  
        self.y = j * COLUMN_WIDTH + (j + 1) * COLUMN_GAP + TOP_GAP
        self.visited = False
        self.pathFrom = []
        self.cost = 0
        self.color = (255, 255, 255)
        self.parent = None
        pass
    
    def draw(self,screen, color = None):
        if color == None:
            color = self.color 
        pygame.draw.rect(screen, color, (self.x, self.y, ROW_WIDTH, COLUMN_WIDTH))

    def setVisited(self):
        self.visited = True
    
    def addPath(self, node):
        if node not in self.pathFrom:
            self.pathFrom.append(node)
            node.addPath(self)
        
    def coordinates(self):
        return self.i, self.j
    
    def distance(self, node):
        return math.sqrt((node.i - self.i) ** 2 + (node.j - self.j) ** 2)

    def setParent(self, node):
        self.parent = node
    
    def getPixel(self):
        return self.x, self.y

class Stack:
    def __init__(self):
        self.__stack = []
        self.stackHead = 0
    
    def push(self, i):
        self.__stack.append(i)
        self.stackHead += 1
    
    def pop(self):
        self.stackHead -= 1
        return self.__stack.pop()
        
    def print(self):
        for n in self.__stack:
            print(n.coordinates())
            
    def pop_back(self):
        n = self.__stack[0]
        self.__stack.remove(n)
        self.stackHead -= 1
        return n
 