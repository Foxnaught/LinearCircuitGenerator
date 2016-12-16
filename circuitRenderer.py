import pickle
import pygame
from linearV4 import groupRecurse
from pygame.locals import *

#For a given circuit configuration, return a surface with a rendering of it
#If the series flag is true then each render in the group should be arranged vertically
#If the series flag is false then each render in the group should be arranged horizontally
#This is a recursive function
def renderCircuit(config, series=True):
	global screen
	#List of renderings
	elementRenders = []

	#Gives statistics for all the sub-renders
	#This allows us to arrange them before returning them
	totalX = 0
	maxX = 0
	totalY = 0
	maxY = 0

	resistorWidth = 8
	resistorHeight = 20

	#For each item in this group
	for element in config:
		#The element in the group is just a simple resistor so just add a simple render
		if element == 1:
			singleRender = pygame.Surface((resistorWidth*2, resistorHeight))
			pygame.draw.rect(singleRender, (255, 255, 255), ((int(resistorWidth/2), 0), (resistorWidth, resistorHeight)))
			elementRenders.append(singleRender)
		#The element in the group also is a group so we will call this function recursively and add the returned render
		else:
			elementRenders.append(renderCircuit(element, series=not series))

	#Find the largest width and height in our list of subrenders
	for e in elementRenders:
		eSize = e.get_size()
		totalX += eSize[0]
		totalY += eSize[1]

		if maxX < eSize[0]:
			maxX = eSize[0]

		if maxY < eSize[1]:
			maxY = eSize[1]

	#The rendering of the whole group that we will return
	circuitRender = 0
	#If the group is in series then render the subrenders vertically
	if series:
		circuitRender = pygame.Surface((maxX, totalY))
		curY = 0
		for i in elementRenders:
			curX = int((maxX-i.get_size()[0])/2)
			circuitRender.blit(i, (curX, curY))
			curY += i.get_size()[1]

	#If the group is in parallel then render the subrenders horizontally
	else:
		circuitRender = pygame.Surface((totalX, maxY))
		curX = 0
		for i in elementRenders:
			curY = int((maxY-i.get_size()[1])/2)
			circuitRender.blit(i, (curX, curY))
			#Draw from the top down to the resistor
			pygame.draw.rect(circuitRender, (255, 0, 0), ((curX+int(i.get_size()[0]/2-resistorWidth/4), 0), (int(resistorWidth/2), curY)))
			#Draw from the top down to the resistor
			pygame.draw.rect(circuitRender, (255, 0, 0), ((curX+int(i.get_size()[0]/2-resistorWidth/4), curY+i.get_size()[1]), (int(resistorWidth/2), curY)))
			curX += i.get_size()[0]

		#Draw the wires for the top and bottom of the parallel group
		firstElem = elementRenders[0]
		lastElem = elementRenders[-1]
		pygame.draw.rect(circuitRender, (255, 0, 0), ((int(firstElem.get_size()[0]/2)-int(resistorWidth/2), 0), (totalX-int(firstElem.get_size()[0]/2), int(resistorWidth/2))))
		pygame.draw.rect(circuitRender, (255, 0, 0), ((int(firstElem.get_size()[0]/2)-int(resistorWidth/2), maxY-int(resistorWidth/2)), (totalX-int(firstElem.get_size()[0]/2), int(resistorWidth/2))))

	return circuitRender




n = int(input("Number of resistors: "))
pList = [1] * n
#Use the function groupRecurse from linearV4.py
circuitList = [pList] + groupRecurse(pList)

pygame.init()
screen = pygame.display.set_mode((640, 480), pygame.DOUBLEBUF)
clock = pygame.time.Clock()
for circuit in circuitList:
	print(circuit)
	spaceBool = False
	while 1:
		#We don't need to update that often for this program
		clock.tick(10)
		screen.fill((0, 0, 0))
		screen.blit(renderCircuit(circuit), (20, 20))

		keyStates = pygame.key.get_pressed()
		if keyStates[K_SPACE]:
			if spaceBool:
				spaceBool = False
				break
		else:
			spaceBool = True

		#Get window events so that it doesn't freeze
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				raise SystemExit

		pygame.display.flip()

print("End")