"""
   .. module: mapgame
    :synopsis: The module that controls the game UI.
"""

import sys, os
import pygame
import numpy as np
import time

# Import the map module
map_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),os.pardir)
if map_path not in sys.path:
    sys.path.append( map_path )

import map
import map.cell as cell
import game.game as game
import game.player as player

pygame.init()
gameDisplay = pygame.display.set_mode((1280,720), pygame.RESIZABLE)
pygame.display.set_caption('HexTowns')

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
YELLOW = (255,255,0)
BLUE = (0,0,255)

def IDtoColor(ID):#Take player ID return color
	if ID == 1:
		return RED
	if ID == 2:
		return GREEN
	if ID == 3:
		return BLUE
	if ID == 4:
		return YELLOW

buttonPosition = np.zeros((8), dtype = (int,2)) #Array for button x,y coordinates, statically defined so change size for new buttons
myfont = pygame.font.SysFont("monospace", 15)
color_dict = {cell.RED: RED, cell.EMPTY: WHITE}

#draws screen
def draw_map(dMap,posGrid):
	draw_grid(dMap,40,100,50,posGrid)
	pygame.display.update()

#creates x by y grid of hexagons starting at startX, startY
def draw_grid(dMap,sideLength,startX,startY,posGrid):
	lead_x = startX
	yDisp = np.sin(np.deg2rad(60))*sideLength
	xDisp = np.cos(np.deg2rad(60))*sideLength
	#i is collumn number q is row number
	for i in range(dMap.getDimensions()[0]):
		if (i % 2) == 0:
			 lead_y = startY
		else:
			lead_y = startY + yDisp + 5
		for q in range(dMap.getDimensions()[1]):
			draw_hex(dMap,sideLength,lead_x,lead_y,i,q)
			posGrid[i,q][0] = lead_x#Sets pixel coordinates for hexs in posGrid
			posGrid[i,q][1] = lead_y
			lead_y += (yDisp*2) + 10
			
		lead_x += sideLength + xDisp + 10
		
	
#Draw individual hexagon
def draw_hex(dMap, sideLength, lead_x, lead_y, hex_x, hex_y):
	xDisp = np.cos(np.deg2rad(60))*sideLength 
	yDisp = np.sin(np.deg2rad(60))*sideLength
	#Shape defined by array of points
	pygame.draw.polygon(gameDisplay,dMap.getRGB((hex_x, hex_y)),
			    [(lead_x,lead_y), (lead_x+sideLength,lead_y),
			     (lead_x+sideLength+xDisp,lead_y+yDisp), (lead_x+sideLength,lead_y+(yDisp*2)),
			     (lead_x,lead_y+(yDisp*2)), (lead_x-xDisp,lead_y+yDisp)])
	if (dMap.getType((hex_x, hex_y)) == 2):
		drawText("T", lead_x + 17, lead_y + (sideLength/2), BLACK)

def button(msg, buttonx, buttony, bPos, buttonID):#Draw Button
	pygame.draw.rect(gameDisplay,WHITE,[buttonx, buttony, 150, 50])
	drawText(msg, buttonx, buttony, BLACK)
	bPos[buttonID][0] = buttonx
	bPos[buttonID][1] = buttony
	
def drawText(msg, msg_x, msg_y, color):
	label = myfont.render(msg, 5, color)
	gameDisplay.blit(label, (msg_x, msg_y))
	
def bChecker(startx, starty, bPos):#Check if click on button
	for i in range(len(bPos)):
		if (startx >= bPos[i][0] and startx <= bPos[i][0] + 150):
			if (starty >= bPos[i][1] and starty <= bPos[i][1] + 50):
				return i;
				
def mapResources(Map):#Allocates resources to tiles
	dim = Map.getDimensions()
	for row in range(dim[0]):
		for col in range(dim[1]):
			Map.setResources((row, col), 1)

def disp_resources(player): #Display curPlayer resources in top right corner
	pygame.draw.rect(gameDisplay, BLACK, [1190, 75, 50, 50])
	res = player.getResources()
	label = ('Resources: %g' % (res))
	drawText(label, 1100, 100, WHITE)
			
def game_start():
	button("Start", 885, 515, buttonPosition, 0)
	button("Exit", 885, 580, buttonPosition, 1)
	pygame.display.update()
	
	gameExit = False
	while not gameExit:#Menu event handler
		for event in pygame.event.get():
			if event.type == pygame.MOUSEBUTTONUP:
				pos = pygame.mouse.get_pos()
				if (bChecker(pos[0], pos[1], buttonPosition) == 0):#Check if mouse is on start button
					gameRun = game.Game(None)
					game_loop()
				if (bChecker(pos[0], pos[1], buttonPosition) == 1):#Check if mouse is on quit button
					gameExit = True
			if event.type == pygame.QUIT:
				gameExit = True

def game_loop():
	#Build map for tests
	dimX = 8 
	dimY = 7
	map1 = map.Map(dimX, dimY)
	posGrid = np.zeros((dimX,dimY), dtype = (int,2))

	map1.setCell((1,1),color=cell.RED, type=cell.TOWER, strength=2)
	map1.setCell((2,1),color=cell.RED, type=cell.UNIT, strength=1)
	map1.setCell((1,5),color=cell.BLUE, type=cell.TOWER, strength=2)
	map1.setCell((2,5),color=cell.BLUE, type=cell.UNIT, strength=1)
	map1.setCell((6,1),color=cell.GREEN, type=cell.TOWER, strength=2)
	map1.setCell((5,1),color=cell.GREEN, type=cell.UNIT, strength=1)
	map1.setCell((6,5),color=cell.YELLOW, type=cell.TOWER, strength=2)
	map1.setCell((5,5),color=cell.YELLOW, type=cell.UNIT, strength=1)

	mapResources(map1)
	
	#Game Variables
	gameExit = False
	moving = False
	building = False
	pos = (-1,-1)
	
	#Game Objects
	game1 = game.Game(map1)
	curPlayer = game1.getCurrentPlayer()
	
	#Draw Buttons and map
	gameDisplay.fill(BLACK)
	button("Move", 750, 300, buttonPosition, 2)
	button("Attack", 925, 300, buttonPosition, 4)
	button("End Turn", 750, 375, buttonPosition, 3)
	button("Build Unit", 925, 375, buttonPosition, 7)
	drawText("Turn:", 800, 175, WHITE)
	pygame.draw.rect(gameDisplay,IDtoColor(curPlayer.getColor()),[800, 200, 50, 50])
	disp_resources(curPlayer)
	draw_map(map1,posGrid)
	
	while not gameExit:#Game event handler
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.MOUSEBUTTONUP:
				mPos = pygame.mouse.get_pos()
				
				if pos != (-1, -1) and (bChecker(mPos[0], mPos[1], buttonPosition) == 2): #Move button
					moving = True
					building = False
					attacking = False
								
				if (bChecker(mPos[0], mPos[1], buttonPosition) == 3): #End Turn
					game1.endTurn()
					curPlayer = game1.getCurrentPlayer()
					pygame.draw.rect(gameDisplay,IDtoColor(curPlayer.getColor()),[800, 200, 50, 50])
					moving = False
					disp_resources(curPlayer)
					pygame.display.update()
					
				if pos != (-1,-1) and (bChecker(mPos[0],mPos[1], buttonPosition) == 4): #Attack button
					attacking = True
					moving = False
					
				if (bChecker(mPos[0], mPos[1], buttonPosition) == 7): #Build unit button
					if ((map1.getType(pos) == 2) and map1.getRGB(pos) == IDtoColor(curPlayer.getColor())): #Only towers can build units and only during their turn
						if (curPlayer.getResources() > 0):
							building = True
							moving = False
							
				for i in range(dimX):#Checks every hex to see if clicked
					for q in range(dimY):
						if (mPos[0] >= posGrid[i,q][0] and mPos[0] <= 40 + posGrid[i,q][0]) and (mPos[1] >= posGrid[i,q][1] and mPos[1] <= 80 + posGrid[i,q][1]):#Checks if clicked on hex i,q
							if moving and pos != (-1,-1):
								if map1.getRGB(pos) == IDtoColor(curPlayer.getColor()):#Only able to move units whose turn it is
									if map1.getType((i,q)) == 1:
										if map1.getColor(pos) == map1.getColor((i,q)):
											pygame.draw.rect(gameDisplay,WHITE,[800, 500, 400, 200])
											drawText("Would you like to combine?", 800, 500, BLACK)
											button("Yes", 800, 550, buttonPosition, 5)
											button("No", 1000,550, buttonPosition, 6)
											pygame.display.update()
											while(moving):
											    for event in pygame.event.get():
													if event.type == pygame.MOUSEBUTTONUP:
														mPos = pygame.mouse.get_pos()
														if (bChecker(mPos[0], mPos[1], buttonPosition) == 5):
															map1.makeMove(pos, (i,q))
															pygame.draw.rect(gameDisplay, BLACK, [800, 500, 400, 200])
															moving = False
														if (bChecker(mPos[0], mPos[1], buttonPosition) == 6):
															pygame.draw.rect(gameDisplay, BLACK, [800, 500, 400, 200])
															moving = False
															
							if moving:
								map1.makeMove(pos, (i,q))
								moving = False
									
							if building and map1.getType((i,q)) == 0: #Only Builds on empty 
								if (i,q) in map1.getAdjacent(pos): #Only builds on adjacent 
									curPlayer.changeResources(-1) #Subtract from players resources
									map1.setCell((i,q),color=cell.RED, type=cell.UNIT, strength=1)
									draw_map(map1, posGrid)
									disp_resources(curPlayer)
									pygame.display.update()
									building = False
							
							pos = (i,q)	
							draw_map(map1, posGrid)
							pygame.display.update()
							
game_start()
