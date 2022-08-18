import random
import pygame
from components import *

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

# start_node = random.choice(nodeList)
start_node = nodeList[0]

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
path_found = False

while run:
    
    nodes = []
    visitedNodes = []
    
    for node in nodeList:
        node.visited = False
        node.cost = 0
        for n in node.pathFrom:
            x = (node.x + n.x) / 2
            y = (node.y + n.y) / 2
            
            #drawing the current node, it parent node and midpoint between them
            node.draw(screen)
            n.draw(screen)
            pygame.draw.rect(screen, (255, 255, 255), (x, y, ROW_WIDTH, COLUMN_WIDTH))        
    
    #keyboard bindings
    for event in pygame.event.get():
        #to close the window
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False
            
        #selecting starting and ending nodes
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            keydown = True
        
        #checking shift + left_mouse_click
        if pygame.mouse.get_pressed(3)[0] and keydown and not mouse_click:
            x, y = pygame.mouse.get_pos()
            x = int(x - x % (COLUMN_WIDTH+ COLUMN_GAP)) / (COLUMN_WIDTH + COLUMN_GAP)
            y = int(y - y % (ROW_WIDTH + ROW_GAP)) / (ROW_WIDTH + ROW_GAP)
            
            path_found = False
            #selecting the starting node
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
        
        #checking left_mouseclick
        elif pygame.mouse.get_pressed(3)[0] and not mouse_click:
            x, y = pygame.mouse.get_pos()
            x = int(x - x % (COLUMN_WIDTH+ COLUMN_GAP)) / (COLUMN_WIDTH + COLUMN_GAP)
            y = int(y - y % (ROW_WIDTH + ROW_GAP)) / (ROW_WIDTH + ROW_GAP)
            
            path_found = False
            #selecting the ending node
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
    
    # if not path_found:
    if not path_found:
        current_node = start_node
        if start_node != None and end_node != None:
            while(current_node != end_node):
                visitedNodes.append(current_node)
                minVal = 1000000
                current_i, current_j = current_node.coordinates()
                # print(current_i, current_j)

                #determing the neighbours
                for i in range(len(DIRECTIONSX)):
                    new_x = current_i + DIRECTIONSX[i]
                    new_y = current_j + DIRECTIONSY[i]
                    
                    if new_y >=0 and new_x >= 0 and new_x < COLUMN and new_y < ROW:
                        
                        for node in nodeList:
                            if node.i == new_x and node.j == new_y and (node not in visitedNodes) and (node in current_node.pathFrom) and (node not in nodes):
                                node.cost += current_node.cost + 1
                                node.setParent(current_node)
                                nodes.append(node)  
                # print(nodes)
                for node in nodes:
                    if node.distance(end_node) < minVal:
                        current_node = node
                        minVal = current_node.cost
        
                
                nodes.remove(current_node)
            path_found = True
            # print('pathfound')
    else:
        current = end_node
        # drawing the path
        while(current != start_node): #looping until the current node is the starting node
            parent = current.parent
            current_x, current_y = current.getPixel()
            parent_x, parent_y = parent.getPixel()
            pygame.draw.circle(screen, (255, 0, 0), (current_x + ROW_WIDTH / 2, current_y + COLUMN_WIDTH / 2), (ROW_WIDTH + COLUMN_WIDTH) / 4)
            pygame.draw.line(screen, (255, 0, 0), (current_x + ROW_WIDTH / 2, current_y + COLUMN_WIDTH / 2), (parent_x + ROW_WIDTH / 2, parent_y + COLUMN_WIDTH / 2),3)
            current = parent
    
    if start_node != None:
            start_node.draw(screen, (255,0,0))
    
    if end_node != None:
        end_node.draw(screen, (0, 0, 255))
    
    pygame.display.update()
    