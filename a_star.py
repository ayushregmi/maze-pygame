from doctest import master
import random

ROW = 9
COL = 9

maze = []

for i in range(ROW):
    line = []
    for j in range(COL):
        if 0 == random.choice(range(3)):
            line.append(1)
        else:
            line.append(0)
    maze.append(line)
    
for m in maze:
    print(m)