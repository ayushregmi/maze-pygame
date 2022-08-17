import random
import pygame
from components import *
import time
import sys

sys.setrecursionlimit(1000000)

pygame.init()

# defining number, size and width of nodes
# ROW = 20
# COLUMN = 40
# ROW_WIDTH = 20
# COLUMN_WIDTH = 20
# ROW_GAP = 2
# COLUMN_GAP = 2
# TOP_GAP = 5
# BOTTOM_GAP = 5
# LEFT_GAP = 5
# RIGHT_GAP = 5
# SCREEN_HEIGHT = ROW * ROW_WIDTH + (ROW + 1) * ROW_GAP + LEFT_GAP * 2
# SCREEN_WIDTH = COLUMN * COLUMN_WIDTH + (COLUMN + 1) * COLUMN_GAP + TOP_GAP * 2
# DIRECTIONSX = [0, 1, 0, -1]
# DIRECTIONSY = [1, 0, -1, 0]   
    
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

for node in nodeList:
    if node.i == start_node.i and node.j == start_node.j:
        # node.draw(screen, (30, 30, 30))
        pass

# temp = []       
# for i in range(len(DIRECTIONSX)):
#     new_x = start_i + DIRECTIONSX[i]
#     new_y = start_j + DIRECTIONSY[i]
#     # print(new_x, new_y)    
    
#     if new_y >=0 and new_x >= 0 and new_x < COLUMN and new_y < ROW:
#         # print(new_x, new_y)
        
#         for node in nodeList:
#             if node.i == new_x and node.j == new_y and not node.visited:
#                 node.draw(screen,(0, 0, 255))
                
#                 temp.append(node)
                
# while(len(temp) != 0):
#     n = random.choice(temp)
#     temp.remove(n)
#     stack.push(n)

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
    
    start_node = stack.pop()
    
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

while run:                
                
    #keyboard bindings
    for event in pygame.event.get():
        #to close the window
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
        
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_LSHIFT):
                pass
            
    
    
    pygame.display.update()
    
    