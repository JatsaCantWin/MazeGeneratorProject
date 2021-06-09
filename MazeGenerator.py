import random
import Tkinter as tk
from functools import partial

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
        global exit
        return ((len(self.openNeighbors())<=1) or ((len(self.openNeighbors())==2) and (exit in self.openNeighbors()) and len(exit.openNeighbors())==0))
    def __repr__(self):
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
    global frontier
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
    global maze
    return maze[y][x]
    
def drill(x):
    global frontier
    global entrance
    global exit
    frontier.remove(x)
    if x.canBeDrilled():
        x.wall = False
        unvisitedNeighbors = x.unvisitedNeighbors()
        if (entrance == x):
            if (entrance.x==exit.x):
                if entrance.y>exit.y:
                    unvisitedNeighbors.remove(getCell(entrance.x, entrance.y-1))
                else:
                    unvisitedNeighbors.remove(getCell(entrance.x, entrance.y+1))
            elif (entrance.y==exit.y):
                if entrance.x>exit.x:
                    unvisitedNeighbors.remove(getCell(entrance.x-1, entrance.y))
                else:
                    unvisitedNeighbors.remove(getCell(entrance.x+1, entrance.y))
                    
        for i in unvisitedNeighbors:
            i.visited = True
            frontier.append(i)
    
def setupMaze(NA, MA):
    try:
        global selectEntryExit
        global mazeButtons
        global entranceCoord
        global exitCoord
        global N
        global M
        global generated
        NA = int(NA)
        MA = int(MA)
        if (NA>=2) and (NA<=30) and (MA>=2) and (MA<=30):
            N = NA
            M = MA
            generated = False
            for i in mazeButtons:
                for j in i:
                    j.destroy()
               
            mazeButtons = [[tk.Button(width = 2, height = 1, command = partial(clickMazeButton, i, j), bg='#ffffff') for i in range(N)] for j in range(M)]
            for i in range(N):
                for j in range(M):
                    mazeButtons[j][i].place(x=70+i*22, y=j*22)
            selectEntryExit = 0
            entranceCoord=None
            exitCoord=None
            generateButton.place(x = 0, y=63)
        else:
            print("Rozmiar kazdej stany labiryntu musi byc wieksza niz jeden i mniejsza badz rowna 30")
    except:
        print("Podaj poprawny rozmiar labiryntu")
        return
        
def generateMaze():
    global frontier
    global selectEntryExit
    global entranceCoord
    global exitCoord
    global entrance
    global exit
    global maze
    global midpoints
    global generated
    
    if (entranceCoord == None) or (exitCoord == None):
        print("Nalezy wybrac wejscie i wyjscie")
        return
    maze = [[cell(i, j) for i in range(N)] for j in range(M)]
    entrance = getCell(entranceCoord[0], entranceCoord[1])
    exit = getCell(exitCoord[0], exitCoord[1])
    if (exit in entrance.neighbors()):
        print("Wejscie nie moze znajdowac sie kolo wyjscia")
        return
    selectEntryExit=-1
    exit.wall = False
    exit.visited = True
    entrance.visited = True
    frontier = [entrance]
    while len(frontier)>0:
        drill(frontier[random.randint(0, len(frontier)-1)])
        
    generated = True
    
    midpoints = []
        
    origin = entrance
    path = []
    for i in midpoints:
        destination = i
        path.extend(bfs(origin, destination))
        origin = destination
        
    path.extend(bfs(origin, exit))

    for i in path:
        i.path = True  
      
    for i in maze:
        for j in i:
            if j.wall:
                mazeButtons[j.y][j.x].config(bg='#000000')
            elif j not in {entrance, exit}:
                if j.path:
                    mazeButtons[j.y][j.x].config(bg='#ffff00')
                else:
                    mazeButtons[j.y][j.x].config(bg='#ffffff')
        
def clickMazeButton(x, y):
    #print(x)
    #print(y)
    global entranceCoord
    global exitCoord
    global entrance
    global exit
    global selectEntryExit
    global N
    global M
    global midpoints
    global generated
    if generated == True:
        if (entrance!=getCell(x, y)) and (exit!=getCell(x, y)) and (getCell(x, y).wall==False):
            if getCell(x, y) in midpoints:
                mazeButtons[y][x].config(bg='#ffffff')
                midpoints.remove(getCell(x, y))
            else:
                mazeButtons[y][x].config(bg='#ffa500')
                midpoints.append(getCell(x, y))
            for i in maze:
                for j in i:
                    j.path = False
                
            origin = entrance
            path = []
            for i in midpoints:
                destination = i
                path.extend(bfs(origin, destination))
                origin = destination
                
            path.extend(bfs(origin, exit))

            for i in path:
                i.path = True  
            for i in maze:
                for j in i:
                    if (j.wall==False) and (j not in {entrance, exit}) and (j not in midpoints):
                        if j.path:
                            mazeButtons[j.y][j.x].config(bg='#ffff00')
                        else:
                            mazeButtons[j.y][j.x].config(bg='#ffffff')
    else:
        if (x==0) or (x==N-1) or (y==0) or (y==M-1):
            if selectEntryExit==0:
                if (x, y) == exitCoord:
                    print("Wejscie i wyjscie nie moze znajdowac sie w jednym polu")
                    return
                if entranceCoord!= None:
                    mazeButtons[entranceCoord[1]][entranceCoord[0]].config(bg ='#ffffff')
                entranceCoord = (x, y)
                mazeButtons[y][x].config(bg ='#ff1944')
                selectEntryExit=1
            elif selectEntryExit==1:
                if (x, y) == entranceCoord:
                    print("Wejscie i wyjscie nie moze znajdowac sie w jednym polu")
                    return
                if exitCoord!= None:
                    mazeButtons[exitCoord[1]][exitCoord[0]].config(bg ='#ffffff')
                exitCoord = (x, y) 
                mazeButtons[y][x].config(bg ='#19ff44')
                selectEntryExit=0
  
window = tk.Tk()
        
window.geometry("750x680")
        
mazeButtons = []
widthLabel = tk.Label(text = "Width:")
widthEntry = tk.Entry(width = 2)
heightLabel = tk.Label(text = "Height:")
heightEntry = tk.Entry(width = 2)
prepareButton = tk.Button(text = "Prepare", width = 8, command=lambda: setupMaze(widthEntry.get(), heightEntry.get()))
generateButton = tk.Button(text = "Generate", width = 8, command=lambda: generateMaze())

widthLabel.place(x = 0, y=0)
widthEntry.place(x = 50, y=0)
heightLabel.place(x = 0, y=17)
heightEntry.place(x = 50, y=17)
prepareButton.place(x = 0, y=40)

widthEntry.insert(0, "10")
heightEntry.insert(0, "10")

selectEntryExit = -1
generated = False

window.mainloop()