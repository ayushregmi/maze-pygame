
import random
import pygame
from components import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("window")

nodeList = []

for i in range(COLUMN):
    row = []
    for j in range(ROW):
        row.append(Node(i, j))
    nodeList.append(row)


visitedCells = 1

currentCell = nodeList[random.choice(range(COLUMN))][random.choice((range(ROW)))]

stack = Stack()

while visitedCells < ROW * COLUMN:
    currentCell.setVisited()
    neighbours = []
    x, y = currentCell.coordinates()
    for i in range(len(DIRECTIONSX)):
        nx = x + DIRECTIONSX[i]
        ny = y + DIRECTIONSY[i]
        
        if nx >= 0 and nx < COLUMN and ny >= 0 and ny < ROW and not nodeList[nx][ny].visited:
            neighbours.append(nodeList[nx][ny])
    if(len(neighbours) == 0):
        currentCell = stack.pop()
    else:
        stack.push(currentCell)
        current = random.choice(neighbours)

        currentCell.addPath(current)

        currentCell = current

        visitedCells += 1
        

    pass

mouse_click = False
x, y = (0, 0)


start_node = None
end_node = None
keydown = False
path_found = False

run = True
while run:
    for row in nodeList:
        for node in row:
            node.visited = False
            node.draw(screen, (0, 0, 100))
            x, y = node.getPixel()
            for n in node.pathFrom:
                nx, ny = n.getPixel()
                
                pygame.draw.rect(screen, (0, 0, 100), ((x + nx)/2, (y+ny)/2, ROW_WIDTH, COLUMN_WIDTH))
            

    
    nodes = []
    visitedNodes = []
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
                for row in nodeList:
                    for node in row:
                        if(node.i == x and node.j == y):
                            start_node = node
            else:
                if(x, y) == (start_node.i, start_node.j):
                    start_node = None
                else:
                    for row in nodeList:
                        for node in row:
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
                for row in nodeList:
                    for node in row:
                        if(node.i == x and node.j == y):
                            end_node = node
            else:
                if(x, y) == (end_node.i, end_node.j):
                    end_node = None
                else:
                    for row in nodeList:
                        for node in row:
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
            stack = Stack()
            while(current_node != end_node):
                minValue = 1000000
                canVisit = []
                
                for node in current_node.pathFrom:
                    if not node.visited:
                        canVisit.append(node)
                
                if len(canVisit) != 0:
                    for node in canVisit:
                        if node.distance(end_node) < minValue:
                            n = node
                    
                    n.setVisited()
                    stack.push(current_node)
                    n.setParent(current_node)
                    current_node = n
                else:
                    current_node = stack.pop()

            path_found = True
            # print('pathfound')
    else:
        current = end_node
        # drawing the path
        while(current != start_node): #looping until the current node is the starting node
            parent = current.parent
            current_x, current_y = current.getPixel()
            parent_x, parent_y = parent.getPixel()
            # pygame.draw.circle(screen, (255, 0, 0), (current_x + ROW_WIDTH / 2, current_y + COLUMN_WIDTH / 2), (ROW_WIDTH + COLUMN_WIDTH) / 8)
            pygame.draw.line(screen, (100, 0, 0), (current_x + ROW_WIDTH / 2, current_y + COLUMN_WIDTH / 2), (parent_x + ROW_WIDTH / 2, parent_y + COLUMN_WIDTH / 2),3)
            current = parent
    
    if start_node != None:
            start_node.draw(screen, (255,0,0))
    
    if end_node != None:
        end_node.draw(screen, (0, 0, 255))


    pygame.display.update()

