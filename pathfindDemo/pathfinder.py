#TODO
#put Node class in a separate file

import pygame, math

#window
pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 600
GAME_WIDTH = 600

rows = 30
cols = 30

grid = [] #2d array of arrays of Nodes
openList = [] #options to check
closedList = [] #checked options
path = [] #path of nodes

w = GAME_WIDTH // cols
h = SCREEN_HEIGHT // rows

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#node class - nodes the algorithm will traverse on
class Node:
    def __init__(self, horizpos, vertipos):
        self.x = horizpos
        self.y = vertipos
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.nodeState = 0
        self.parent = None
    
    def show(self, screen, color):
        if self.nodeState == 1:
            color = (0,0,0)
        pygame.draw.rect(screen, color, (self.x*w, self.y*h, w-1, h-1))

    def addNeighbors(self, grid):
        if self.x < cols - 1:
            self.neighbors.append(grid[self.x+1][self.y]) #if space to right, append right
        if self.x > 0:
            self.neighbors.append(grid[self.x-1][self.y]) #if space to left, append left
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y+1]) #if space to bottom, append bottom
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y-1]) #if space to top, append top
        #Add Diagonals
        if self.x < cols - 1 and self.y < rows - 1:
            self.neighbors.append(grid[self.x+1][self.y+1]) #bottom right
        if self.x < cols - 1 and self.y > 0:
            self.neighbors.append(grid[self.x+1][self.y-1]) #top right
        if self.x > 0 and self.y < rows - 1:
            self.neighbors.append(grid[self.x-1][self.y+1]) #bottom left
        if self.x > 0 and self.y > 0:
            self.neighbors.append(grid[self.x-1][self.y-1]) #top left
#-----------------------------------------------------------------------------------------------------------#
def changeNodeState(pos, newState):
    x = pos[0] // w
    y = pos[1] // h
    if x <= 29: #brute force to ensure area outside is not selected
        grid[x][y].nodeState = newState

def getNodeState(pos):
    x = pos[0] // w
    y = pos[1] // h
    if x <= 29:
        return grid[x][y].nodeState


def heuristicCalc(start, end):
    return math.sqrt((start.x - end.x)**2 + abs(start.y - end.y)**2)

def setupNodes():
    for i in range(cols):
        array = []
        for j in range(rows):
            array.append(Node(i, j)) #array of all nodes which are created with cords
        grid.append(array)

#gives each node neighbors
    for i in range(cols):
        for j in range(rows):
            grid[i][j].addNeighbors(grid)
#-----------------------------------------------------------------------------------------------------------#
#Setup
setupNodes()
placeState = 1 #walls are placed by default
startNode = grid[0][0]
endNode = grid[29][29]
run = True
startPathing = False
complete = False
fail = False
menuColor = (221, 221, 221)
#draw menu and buttons
#TODO alot of variables(objects) can be reused here
pygame.draw.rect(screen, menuColor, (600, 0, 100, 600))
pygame.draw.rect(screen, (255, 255, 0), (602, 2, 96, 38)) #start button
startFont = pygame.font.SysFont('Corbel', 20)
startText = startFont.render('start', True, (0, 220, 0))
screen.blit(startText, (630, 10))
pygame.draw.rect(screen, (255, 10, 20), (602, 40, 96, 38)) #end button
endFont = pygame.font.SysFont("Corbel", 20)
endText = startFont.render('end', True, (0, 0, 0))
screen.blit(endText, (632, 50))
#TODO wall button 
#-----------------------------------------------------------------------------------------------------------#

#event loop
while run:
#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT: #X button press event
            run = False
        mouse = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if placeState == 1:
                    changeNodeState(pygame.mouse.get_pos(), 1)
                #TODO impliment other placeStates here (start end)
            if pygame.mouse.get_pressed()[2]: #rmb is universal delete
                changeNodeState(pygame.mouse.get_pos(), 0)
            if pygame.mouse.get_pressed()[0] and 601 <= mouse[0] <= 699 and 1 <= mouse[1] <= 37:
                placeState = 2
                print("you would now place start")
                #changeNodeState(pygame.mouse.get_pos(), 2)
            if pygame.mouse.get_pressed()[0] and 601 <= mouse[0] <= 699 and 40 <= mouse[1] <= 78:
                placeState = 3
                print("you would now place ends")

        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                if placeState == 1:
                    changeNodeState(pygame.mouse.get_pos(), 1)
                #TODO add other place states here
            if pygame.mouse.get_pressed()[2]:
                changeNodeState(pygame.mouse.get_pos(), 0)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                openList.append(startNode) #grad current startNode
                startPathing = True
        if event.type == pygame.KEYDOWN and (complete == True or fail == True):
            if event.key == pygame.K_RETURN:
                #reset everything
                for i in range(cols):
                    for j in range(rows):
                        node = grid[i][j]
                        node.f, node.g, node.h = 0, 0, 0
                        node.parent = None
                startPathing = False
                complete = False
                fail = False
                openList = []
                closedList = []
                path = []
                openList.append(startNode)

                
    #end event handler

    #A star algorithm
    
    if startPathing and fail == False:
        if len(openList) > 0:
            bestIndex = 0
            for i in range(len(openList)):
                if openList[i].f < openList[bestIndex].f: #if a better node is found
                    bestIndex = i 
            
            currentNode = openList[bestIndex] #set new best node

            if currentNode == endNode: #pathfind back
                pathBack = currentNode
                while pathBack.parent:
                    path.append(pathBack.parent)
                    pathBack = pathBack.parent
                if not complete:
                    complete = True

                    print("Finish")
                elif complete:
                    continue #dont touch future lines

            if complete == False:
                openList.remove(currentNode)
                closedList.append(currentNode)

                for neighbor in currentNode.neighbors:
                    if neighbor in closedList or neighbor.nodeState == 1:
                        continue #do nothing if currNode has no valid neighbors
                    if currentNode.x != neighbor.x and currentNode.y != neighbor.y:
                        potentialG = currentNode.g + 1.414 #for the sqrt of 2
                    else:
                        potentialG = currentNode.g + 1 #no diagonal
                    
                    #each neighbor's g value has been calculated

                    betterPath = False #assume better path is not found
                    if neighbor in openList: #if neighbor was an traversal option earlier
                        if potentialG < neighbor.g:
                            neighbor.g = potentialG
                            betterPath = True 
                    else:
                        neighbor.g = potentialG #if it wasnt an earlier option give it its g value
                        betterPath = True
                        openList.append(neighbor) #add it to list of options

                    #if a better (or new) path was found...
                    if betterPath:
                        neighbor.f = neighbor.g + heuristicCalc(neighbor, endNode)
                        neighbor.parent = currentNode

        else: #the length of the openList is 0 and no solution was ever found
            print("no solution found")
            fail = True

    #screen.fill((0, 20, 20)) #background color
    pygame.draw.rect(screen, (0, 20, 20), (0, 0, 600, 600))

    for i in range(cols): #for each Node
        for j in range(rows):
            grid[i][j].show(screen, (255, 255, 255)) #draws all squares white by default
            if grid[i][j] == startNode or grid[i][j] == endNode:
                grid[i][j].show(screen, (255, 255, 0))
            elif complete and grid[i][j] in path:
                grid[i][j].show(screen, (25, 120, 255))
            elif grid[i][j] in closedList:
                grid[i][j].show(screen, (255, 0, 0))
            elif grid[i][j] in openList:
                grid[i][j].show(screen, (0, 255, 0))
            elif grid[i][j] == startNode or grid[i][j] == endNode:
                grid[i][j].show(screen, (255, 255, 0))
            
    pygame.display.update()

pygame.quit()