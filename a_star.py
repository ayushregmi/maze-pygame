from queue import LifoQueue


ROW = 9
COL = 9

maze = []

for i in range(ROW):
    line = []
    for j in range(COL):
        line.append(0)
    maze.append(line)

for i in range(ROW):
    print(maze[i])