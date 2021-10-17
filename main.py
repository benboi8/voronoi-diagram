import sys
sys.path.insert(1, "/Python Projects/GuiObjects")

from GUIObjects import *

import random
from math import *
import numpy as np

# create screen
width, height = 400, 400
sf = 2
screen = pg.display.set_mode((width * sf, height * sf))

screen.fill(darkGray)
pg.display.update()

# draw everything
def DrawLoop():
	# fill screen
	# screen.fill(darkGray)

	# draw gui objects
	DrawGui()

	v.Draw()

	pg.display.update()

# quit program
def Quit():
	global running
	running = False

# handle events
def HandleEvents(event):
	# handle gui events
	HandleGui(event)


class Point:
	def __init__(self, pos, radius, color):
		self.pos = pos
		self.radius = radius
		self.color = color

	def Draw(self):
		pg.draw.circle(screen, black, self.pos, self.radius + 1)
		pg.draw.circle(screen, self.color, self.pos, self.radius)

	def GetEuclideanDistanceToPoint(self, x, y):
		return sqrt((self.pos[0] - x) ** 2 + (self.pos[1] - y) ** 2)

	def GetTaxicabDistanceToPoint(self, x, y):
		return abs(x - self.pos[0]) + abs(y - self.pos[1])


class Voronoi:
	def __init__(self, colors, positions=[], radius=2):
		self.colors = colors
		self.numOfPoints = len(colors)
		self.radius = radius * sf
		self.expansionRadius = self.radius

		if len(positions) == self.numOfPoints:
			self.positions = positions
		else:
			self.positions = []
			for i in range(self.numOfPoints):
				self.positions.append((random.randint(0, width * sf), random.randint(0, height * sf)))

		self.CreatePoints()

	def CreatePoints(self):
		self.points = []

		for i in range(self.numOfPoints):
			self.points.append(Point(self.positions[i], self.radius, self.colors[i]))

		self.DrawDistances()


	def Draw(self):
		# if self.expansionRadius + 1 <= max(width * sf, height * sf):
			# self.expansionRadius += 1

			# self.ExpandFromPoint()

		for p in self.points:
			p.Draw()

	def DrawDistances(self):
		pixels = []

		for x in range(width * sf):
			for y in range(height * sf):
				closest = (self.points[0].GetTaxicabDistanceToPoint(x, y), self.points[0])

				for p in self.points:
					dist = (p.GetTaxicabDistanceToPoint(x, y), p)
					if closest[0] > dist[0]:
						closest = dist

				pixels.append((x, y, closest[1].color))

		for p in pixels:
			pg.gfxdraw.pixel(screen, p[0], p[1], p[2])

	def ExpandFromPoint(self):
		for x in range(width * sf):
			for y in range(height * sf):
				distances = []
				for p in self.points:
					dx = abs(x - p.pos[0])
					dy = abs(y - p.pos[1])

					if dx ** 2 + dy ** 2 <= self.expansionRadius ** 2:
						distances.append((p.GetEuclideanDistanceToPoint(x, y), p))
						# distances.append((p.GetTaxicabDistanceToPoint(x, y), p))

				if len(distances) > 0:
					closest = distances[0]
					for d in distances:
						if closest[0] > d[0]:
							closest = d

					pg.gfxdraw.pixel(screen, x, y, closest[1].color)


colors = []
for i in range(25):
	colors.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
v = Voronoi(colors)


while running:
	# tick clock at fps
	clock.tick_busy_loop(fps)

	# get all events
	for event in pg.event.get():
		# check for quit events
		if event.type == pg.QUIT:
			Quit()

		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				Quit()

		HandleEvents(event)

	DrawLoop()

