import random

showCoords = False

class cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = True
        self.visited = False
        self.path = False
    def neighbors(self):
        result = []
        result.extend([getCell(i, self.y) for i in {self.x-1, self.x+1} if i>=0 and i<=N-1])
        result.extend([getCell(self.x, i) for i in {self.y-1, self.y+1} if i>=0 and i<=M-1])
        return result
    def unvisitedNeighbors(self):
        return [i for i in self.neighbors() if i.visited == False]
    def openNeighbors(self):
        return [i for i in self.neighbors() if i.wall == False]
    def canBeDrilled(self):
        return ((len(self.openNeighbors())<=1) or ((len(self.openNeighbors())==2) and (exit in self.openNeighbors()) and len(exit.openNeighbors())==0))
    def __repr__(self):
        if showCoords:
            return "({} {})".format(self.x, self.y)
        if self.path:
            return "^"
        if self.visited:
            if self.wall:
                return "X"
            else:
                return "O"
        else:
            if self.wall:
                return "x"
            else:
                return "o"
            
def bfs(origin, destination):
    result = []
    frontier = []
    frontier.append(origin)
    cameFrom = dict()
    cameFrom[origin] = None
    
    while len(frontier)>0:
        for i in frontier[0].openNeighbors():
            if i not in cameFrom:
                frontier.append(i)
                cameFrom[i]=frontier[0]
        del frontier[0]
    head = destination
    while head!=origin:
        result.append(head)
        head = cameFrom[head]
    result.append(origin)
    return result
    
def getCell(x, y):
    return maze[y][x]
    
def drill(x):
    frontier.remove(x)
    if x.canBeDrilled():
        x.wall = False
        for i in x.unvisitedNeighbors():
            i.visited = True
            frontier.append(i)
    
N = 10
M = 10
maze = [[cell(i, j) for i in range(N)] for j in range(M)]
    
entranceCoord = (0, 0)
exitCoord = (N-1, 4)
midPoints = [getCell(2, 8), getCell(N-4, M-4)]

entrance = getCell(entranceCoord[0], entranceCoord[1])
exit = getCell(exitCoord[0], exitCoord[1])
exit.wall = False
exit.visited = True
entrance.visited = True
frontier = [entrance]

random.seed(10)

while len(frontier)>0:
    drill(frontier[random.randint(0, len(frontier)-1)])
    
for i in maze:
    print(i)
    
origin = entrance
path = []
for i in midPoints:
    destination = i
    path.extend(bfs(origin, destination))
    origin = destination
    
path.extend(bfs(origin, exit))

for i in path:
    i.path = True
print()
print()
print()
for i in maze:
    print(i)