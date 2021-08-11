import pygame, sys, time
from pygame.locals import *


BLACK = (0,0,0)
WHITE = (255,255,255)
Started = False

ShowGridLines = True 


class Window():
    def __init__(self, WW, WH, Name):
        self.WW = WW
        self.WH = WH
        self.Name = Name
    
    def initWindow(self):
        pygame.init()
        self.WindowSurface = pygame.display.set_mode((self.WW,self.WH),0,32)
        pygame.display.set_caption(self.Name)

##WHOLE GRID##
class Grid():
    def __init__(self,width, height):
        self.width = width
        self.height = height
        self.squares = []
        self.objects = []

    def populate(self):
        for i in range(1,self.height + 1):
            for j in range(1,self.width + 1):
                self.squares.append(Square(j,i))
    
    def reset(self):
        #Access global Started variable
        global Started
        #Edits for all
        Started = False

        for i in self.squares:
            i.state = "dead"
            i.nextMove = "die"
            i.Update()

##INDUVIDUAL SQUARES##
class Square():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.state = "dead"
        self.colour = BLACK
        self.nextMove = "maintain"
        self.nearAlive = 0
    
    #Check how many surrounding cells are alive
    def CheckNear(self,grid,gridy):
        self.nearAlive = 0
        #above
        if self.y != 1:
            for i in range(1,3):
                if grid.squares[grid.squares.index(self)-51 + i].state == "alive":
                    self.nearAlive += 1
            if self.x > 1:
                if grid.squares[grid.squares.index(self)-51].state =="alive":
                    self.nearAlive += 1
        #left
        if self.x > 1:
            if grid.squares[grid.squares.index(self) - 1].state == "alive":
                self.nearAlive += 1
        #right
        if self.x < 50:
            if grid.squares[grid.squares.index(self) + 1].state == "alive":
                self.nearAlive += 1
        #below
        if self.y < gridy:
            for i in range(1,3):
                if grid.squares[grid.squares.index(self)+48 + i].state == "alive":
                    self.nearAlive += 1
            if self.x < 50:
                if grid.squares[grid.squares.index(self)+51].state == "alive":
                    self.nearAlive += 1
    
    def CalcChange(self):
        if self.state == "alive":
            if self.nearAlive < 2:
                self.nextMove = "die"
            elif self.nearAlive == 2 or self.nearAlive == 3:
                self.nextMove = "maintain"
            elif self.nearAlive > 3:
                self.nextMove = "die"
        else:
            if self.nearAlive == 3:
                self.nextMove = "live"
            else:
                self.nextMove = "maintain"
    
    def Update(self):
        if self.nextMove == "die":
            self.state = "dead"
            self.colour = BLACK
        elif self.nextMove == "live":
            self.state = "alive"
            self.colour = WHITE
        elif self.nextMove == "maintain":
            self.state = self.state
    
    def Clicked(self,grid):
        if Started == False:
            if self.state == "dead":
                self.state = "alive"
                self.colour = WHITE
            else:
                self.state = "dead"
                self.colour = BLACK
        else:
            if self.x == 50 and self.y == 50:
                grid.reset()


window = Window(500,500,"Game Of Life")
window.initWindow()
gridx = 50
gridy = 50
grid = Grid(gridx,gridy)
grid.populate()
for i in grid.squares:
    grid.objects.append(pygame.Rect((i.x - 1) * (window.WW/gridx), (i.y - 1) * (window.WH/gridy), window.WW/gridx, window.WH/gridy))

#GridLines
gridlines = []
for i in range(1,gridx):
    gridlines.append(pygame.Rect((i *10) - 1, 0, 2, window.WH))
for i in range(1,gridy):#
    gridlines.append(pygame.Rect(0, (i * 10) - 1, window.WW, 2))

while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            for rect in grid.objects:
                if rect.collidepoint((x,y)):
                    grid.squares[grid.objects.index(rect)].Clicked(grid)
    
    for i in grid.objects:
        pygame.draw.rect(window.WindowSurface,grid.squares[grid.objects.index(i)].colour,i)

    if grid.squares[0].state == "alive" and Started == False:
        Started = True

    if Started == True:
        for i in grid.squares:
            i.CheckNear(grid,gridy)
            i.CalcChange()
        for i in grid.squares:
            i.Update()

    if ShowGridLines == True:
        for i in gridlines:
            pygame.draw.rect(window.WindowSurface,(50,50,50),i)






    pygame.display.update()
    if Started == False:
        time.sleep(0.02)
    else:
        time.sleep(0.05)
