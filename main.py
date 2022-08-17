from operator import truediv
import random
from tracemalloc import start
from turtle import right
import pygame
from components import *
import time
import sys

# sys.setrecursionlimit(1000000)

pygame.init()
#initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("maze")


#stack for depth first search
stack = Stack()

#contains all the nodes 1-dimensional
nodeList = []

#creating the nodes and appending them
for i in range(COLUMN):
        x = i * ROW_WIDTH + (i + 1) * ROW_GAP + LEFT_GAP
        y = 0
        
        for j in range(ROW):
            y = j * COLUMN_WIDTH + (j + 1) * COLUMN_GAP + TOP_GAP
            nodeList.append(Node(i, j))

#drawing the nodes for depth first search
# for node in nodeList:
#     node.draw(screen)

run = True

start_node = random.choice(nodeList)

while True:
    start_i, start_j = start_node.coordinates()
    temp = []
    for i in range(len(DIRECTIONSX)):
        new_x = start_i + DIRECTIONSX[i]
        new_y = start_j + DIRECTIONSY[i]
        
        if new_y >=0 and new_x >= 0 and new_x < COLUMN and new_y < ROW:
            
            for node in nodeList:
                if node.i == new_x and node.j == new_y and not node.visited:
                    # node.draw(screen,(0, 0, 255))
                    x = (start_node.x + node.x) / 2
                    y = (start_node.y + node.y) / 2
                    # pygame.draw.rect(screen, (0, 0, 255), (x, y, ROW_WIDTH, COLUMN_WIDTH))
                    
                    node.setVisited()
                    start_node.addPath(node)
                    temp.append(node)
        
    while(len(temp) != 0):
        n = random.choice(temp)
        temp.remove(n)
        stack.push(n)
    
    i = random.choice(range(2))
    start_node = stack.pop() if i != 1 else stack.pop_back()
    
    if(stack.stackHead == 0):
        break
    
    
# print(nodeList[1].pathFrom)

for node in nodeList:
    for n in node.pathFrom:
        x = (node.x + n.x) / 2
        y = (node.y + n.y) / 2
        
        #drawing the current node, it parent node and midpoint between them
        node.draw(screen)
        n.draw(screen)
        pygame.draw.rect(screen, (255, 255, 255), (x, y, ROW_WIDTH, COLUMN_WIDTH))

mouse_click = False
x, y = (0, 0)


start_node = None
end_node = None
keydown = False

while run:
       
    nodes = []
    visitedNodes = []
    
    for node in nodeList:
        for n in node.pathFrom:
            x = (node.x + n.x) / 2
            y = (node.y + n.y) / 2
            
            #drawing the current node, it parent node and midpoint between them
            node.draw(screen)
            n.draw(screen)
            pygame.draw.rect(screen, (255, 255, 255), (x, y, ROW_WIDTH, COLUMN_WIDTH))        
    
    if start_node != None:
            start_node.draw(screen, (255,0,0))
    
    if end_node != None:
        end_node.draw(screen, (0, 0, 255))
    #keyboard bindings
    for event in pygame.event.get():
        #to close the window
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
            
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            keydown = True
        
        if pygame.mouse.get_pressed(3)[0] and keydown and not mouse_click:
            x, y = pygame.mouse.get_pos()
            x = int(x - x % (COLUMN_WIDTH+ COLUMN_GAP)) / (COLUMN_WIDTH + COLUMN_GAP)
            y = int(y - y % (ROW_WIDTH + ROW_GAP)) / (ROW_WIDTH + ROW_GAP)
            
            if(start_node == None):
                for node in nodeList:
                    if(node.i == x and node.j == y):
                        start_node = node
            
            else:
                if(x, y) == (start_node.i, start_node.j):
                    start_node = None
                else:
                    for node in nodeList:
                        if(node.i == x and node.j == y):
                            start_node = node
                
            
            mouse_click = True
        
        elif pygame.mouse.get_pressed(3)[0] and not mouse_click:
            x, y = pygame.mouse.get_pos()
            x = int(x - x % (COLUMN_WIDTH+ COLUMN_GAP)) / (COLUMN_WIDTH + COLUMN_GAP)
            y = int(y - y % (ROW_WIDTH + ROW_GAP)) / (ROW_WIDTH + ROW_GAP)
            
            if(end_node == None):
                for node in nodeList:
                    if(node.i == x and node.j == y):
                        end_node = node
            
            else:
                if(x, y) == (end_node.i, end_node.j):
                    end_node = None
                else:
                    for node in nodeList:
                        if(node.i == x and node.j == y):
                            end_node = node
            mouse_click = True
        
        if not pygame.mouse.get_pressed(3)[0] and mouse_click:
            mouse_click = False
        
        if event.type == pygame.KEYUP:
            keydown = False
    
    visitedNodes.append(start_node)
    if start_node != None and end_node != None:
        while(start_node != end_node):
            minVal = 0
            start_i, start_j = start_node.coordinates()
            temp = []
            for i in range(len(DIRECTIONSX)):
                new_x = start_i + DIRECTIONSX[i]
                new_y = start_j + DIRECTIONSY[i]
                
                if new_y >=0 and new_x >= 0 and new_x < COLUMN and new_y < ROW:
                    
                    for node in nodeList:
                        if node.i == new_x and node.j == new_y and (node not in visitedNodes) and (node in start_node.pathFrom) and (node not in nodes):
                            node.cost += start_node + 2
                            nodes.append(node)
                        
    
            for node in nodes:
                
                pass
    
    pygame.display.update()
    
    