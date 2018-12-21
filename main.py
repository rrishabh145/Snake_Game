#Snake game python

import math
import random
import pygame
import tkinter as tk
from tkinter import messagebox

class cube(object):
	rows = 20
	w = 500
	def __init__(self, start, dirnx=1, dirny=0, color=(255,0,0)):
		self.pos = start
		self.dirnx = 1
		self.dirny = 0
		self.color = color

	def move(self, dirnx, dirny): #changing the direction of the cube so that it stays with the object
		self.dirnx = dirnx 
		self.dirny = dirny
		self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny) #chang our position

	def draw(self, surface, eyes=False):
		dis = self.w // self.rows #distance between the lines
		i = self.pos[0] #rows
		j = self.pos[1] #coloumns

		pygame.draw.rect(surface,self.color, (i*dis+1, j*dis+1, dis-2,dis-2))#draw a rectangle a bit smaller than the actual size of the grid
		if eyes: #making eyes for the snake head
			centre = dis//2
			radius = 3
			circleMiddle = (i*dis+centre-radius, j*dis+8)
			circleMiddle2 = (i*dis+dis-radius*2, j*dis+8)
			pygame.draw.circle(surface, (0,0,0),circleMiddle, radius)
			pygame.draw.circle(surface, (0,0,0),circleMiddle2, radius)
			
class snake(object):
	body = [] #list to keep track of the body of snake
	turns = {} #to check the turns taken by the snake
	def __init__(self, color, pos):
		self.color = color
		self.head = cube(pos)
		self.body.append(self.head) #the body of snake starts with the head
		self.dirnx = 0 #0 or 1 or -1 to depict direction of the snake for axes
		self.dirny = 1
	
	def move(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #to check if the cross button is pressed, the game closes
				pygame.quit()

			keys = pygame.key.get_pressed() #checks which key is pressed

			for key in keys:
				if keys[pygame.K_LEFT]:
					self.dirnx = -1 #change the direction of x towards left
					self.dirny = 0 #keep the y same
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] #storing the position there head turned

				elif keys[pygame.K_RIGHT]:
					self.dirnx = 1 
					self.dirny = 0 
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] #storing the position there head turned

				elif keys[pygame.K_UP]:
					self.dirnx = 0 
					self.dirny = -1
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] #storing the position there head turned

				elif keys[pygame.K_DOWN]:				
					self.dirnx = 0 
					self.dirny = 1 
					self.turns[self.head.pos[:]] = [self.dirnx, self.dirny] #storing the position there head turned

		for i, c in enumerate(self.body):
			p = c.pos[:]
			if p in self.turns:
				turn = self.turns[p]
				c.move(turn[0],turn[1])
				if i == len(self.body)-1:
					self.turns.pop(p)
			else:
				if c.dirnx == -1 and c.pos[0] <=0: c.pos = (c.rows-1, c.pos[1])
				elif c.dirnx == 1 and c.pos[0]>=c.rows-1: c.pos = (0, c.pos[1])
				elif c.dirny == 1 and c.pos[1]>= c.rows-1: c.pos = (c.pos[0],0)
				elif c.dirny == -1 and c.pos[1]<= 0: c.pos = (c.pos[0],c.rows-1)
				else: c.move(c.dirnx, c.dirny)

	def reset(self, pos): #resetting the snake
		self.head = cube(pos)
		self.body = []
		self.body.append(self.head)
		self.turns = {}
		self.dirnx = 0
		self.dirny = 1

	def addCube(self):
		tail = self.body[-1]
		dx, dy = tail.dirnx, tail.dirny #direction of x and y

		#check what direction the head is moving to and add the new cube in that direction
		if dx == 1 and dy==0:
			self.body.append(cube((tail.pos[0]-1,tail.pos[1])))
		elif dx==-1 and dy==0:
			self.body.append(cube((tail.pos[0]+1,tail.pos[1])))
		elif dx==0 and dy==1:
			self.body.append(cube((tail.pos[0],tail.pos[1]-1)))
		elif dx==0 and dy==-1:
			self.body.append(cube((tail.pos[0],tail.pos[1]+1)))

		self.body[-1].dirnx = dx #set the direction of the new cube to the direction of the tail
		self.body[-1].dirny = dy

	def draw(self,surface):
		for i,c in enumerate(self.body):
			if i == 0:
				c.draw(surface, True)
			else:
				c.draw(surface)


def drawGrid(w, rows, surface):
	sizeBetween = w // rows # number of lines we need to have in between the width

	x = 0
	y = 0
	for l in range(rows):
		#update the x and y variables to draw lines one at a time
		x = x+sizeBetween
		y = y+sizeBetween
		
		#draw coloured lines in x and y axes to make a grid
		pygame.draw.line(surface, (255,255,255), (x,0), (x,w))
		pygame.draw.line(surface, (255,255,255), (0,y), (w,y))

def redrawWindow(surface):
	global width, rows, s, snack
	surface.fill((0,0,0)) #the background colour of the game window
	s.draw(surface)
	snack.draw(surface)
	drawGrid(width, rows, surface) #creating a grid
	pygame.display.update() 

def randomSnack(rows,item):
	positions = item.body #positions where the snake body is

	while True:
		x = random.randrange(rows) #randomly picking the coordinates
		y = random.randrange(rows)

		#making a filtered list to check if a cube is not seleted which is snakes body
		if len(list(filter(lambda z:z.pos == (x,y), positions)))>0: 
			continue
		else:
			break

	return (x,y)

def message_box(subject, content): #create a messagebox to display message on top of the game window
	root = tk.Tk()
	root.attributes("-topmost",True) #display on top of other windows
	root.withdraw()
	messagebox.showinfo(subject,content) #shows info
	try:
		root.destroy()
	except:
		pass

def main():
	global width, rows, s, snack
	width = 500 #width of the window
	rows = 20 #no of rows
	win = pygame.display.set_mode((width,width)) #making a square grid
	s = snake((255,0,0),(10,10)) #colour and initial position of the snake
	snack = cube(randomSnack(rows, s), color = (0,255,0)) #calling the snack function
	flag = True

	clock = pygame.time.Clock()

	while flag:
		pygame.time.delay(50) #slowing the snake by adding delay
		clock.tick(10)
		s.move() #check is a key is pressed and move accordingly
		if s.body[0].pos ==snack.pos: #check if head hit the snack
			s.addCube()
			snack = cube(randomSnack(rows, s), color = (0,255,0))

		for x in range(len(s.body)):
			if s.body[x].pos in list(map(lambda z:z.pos,s.body[x+1:])):#check if the cube is in the nody and check for collision 
				print('Score: ',len(s.body))
				message_box('You lost!!!','Play again')
				s.reset((10,10)) #reset if the body hit itself
				break;


		redrawWindow(win) #updating the values and redrawing to show next frame

	pass

main()