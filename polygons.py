import pygame as pg
import numpy as np
import sys
import random
import math
import sympy as sp
from sympy import geometry as sg

BGCOLOR = (0,0,0)
FPS = 60
SCREEN_SHAPE = (400, 300)

VERBOSE = True

NUM_BOIDS = 30
POLYGON_LONG_RADIUS = 8
POLYGON_SHORT_RADIUS = 4
VELOCITY = 1
COHESION_RADIUS = 50
SEPARATION_RADIUS = 50
ALIGNMENT_RADIUS = 50



class Boid:
	def __init__(self, loc):
		self.facing_direction = random.random() * 2. * math.pi

		self.front_tip = sg.Point(*loc).translate(0, POLYGON_LONG_RADIUS).rotate(self.facing_direction, loc)
		self.right_tip = sg.Point(*loc).translate(0, POLYGON_SHORT_RADIUS)\
				.rotate(self.facing_direction + math.pi * 2. / 3., loc)
		self.left_tip = self.right_tip.rotate(math.pi * 2. / 3., loc)
		self.polygon = sg.Triangle(self.front_tip, self.right_tip, self.left_tip)
	
	def move_forward(self):
		displacement = sg.Point(0, VELOCITY).rotate(self.facing_direction)
		self.polygon = self.polygon.translate(displacement.x, displacement.y)
	
	def wrap_around(self):
		if self.polygon.centroid.x < 0:
			self.polygon = self.polygon.translate(SCREEN_SHAPE[0] - 1, 0)
		elif self.polygon.centroid.x >= SCREEN_SHAPE[0]:
			self.polygon = self.polygon.translate(-SCREEN_SHAPE[0], 0)
		if self.polygon.centroid.y < 0:
			self.polygon = self.polygon.translate(0, SCREEN_SHAPE[1] - 1)
		elif self.polygon.centroid.y >= SCREEN_SHAPE[1]:
			self.polygon = self.polygon.translate(0, -SCREEN_SHAPE[1])
	
	def rotate(self, angle):
		self.polygon = self.polygon.rotate(angle, self.polygon.centroid)
		self.facing_direction += angle
	
	def turn_towards(self, point):
		pass

	def dist_boids_within(self, sorted_distances_boids, radius):
		for dist, boid in sorted_distances_boids:
			if dist > radius:
				return
			yield dist, boid
	
	def apply_cohesion(self, distances_boids):
		sum_point = (0., 0.)
		denominator = 0
		for dist, boid in self.dist_boids_within(distances_boids, COHESION_RADIUS):
			sum_point = (sum_point[0] + boid.polygon.centroid.x, sum_point[1] + boid.polygon.centroid.y)
			denominator += 1
		if denominator == 0:
			return # since there's no cohesion to be done
		mean_point = (sum_point[0] / float(denominator), sum_point[1] / float(denominator))
		self.turn_towards(mean_point)

	def apply_separation(self, distances_boids):
		for dist, boid in self.dist_boids_within(distances_boids, SEPARATION_RADIUS):
			#TODO
			pass

	def apply_alignment(self, distances_boids):
		for dist, boid in self.dist_boids_within(distances_boids, ALIGNMENT_RADIUS):
			#TODO
			pass

	def update(self, all_boids):
		self.rotate(0.03)
		#distances = [self.polygon.centroid.distance(b.polygon.centroid) for b in all_boids]
		#distances_boids = zip(distances, all_boids)
		#distances_boids.sort() # so first boids are closest
		#distances_boids = distances_boids[1:] # chop off the first one, since that's this very boid
		distances_boids = []

		self.apply_cohesion(distances_boids)
		self.apply_separation(distances_boids)
		self.apply_alignment(distances_boids)
		self.move_forward()
		self.wrap_around()

	def draw(self, screen):
		#print [(int(v.x), int(v.y)) for v in self.polygon.vertices]
		pg.draw.polygon(screen, (255,255,255), [(int(v.x), int(v.y)) for v in self.polygon.vertices])


all_boids = [Boid((random.random() * SCREEN_SHAPE[0], random.random() * SCREEN_SHAPE[1])) for i in xrange(NUM_BOIDS)]

def draw_all(screen):
	screen.fill(BGCOLOR)
	for boid in all_boids:
		boid.draw(screen)

def update_state(pressed):
	for boid in all_boids:
		boid.update(all_boids)

def process_event(event):
	if event.type == pg.QUIT:
		sys.exit(0)
	elif event.type == pg.KEYDOWN:
		if event.key == pg.K_ESCAPE:
			sys.exit(0)

def setup():
	pass

if True:
	setup()

	clock = pg.time.Clock()
	pg.init()
	screen = pg.display.set_mode(SCREEN_SHAPE)

	try:
		while True:
			for event in pg.event.get():
				process_event(event)

			if VERBOSE: print "updating state..."
			pressed = pg.key.get_pressed()
			update_state(pressed)

			if VERBOSE: print "drawing..."
			draw_all(screen)

			pg.display.flip()
			clock.tick(FPS)
	except KeyboardInterrupt as e:
		sys.exit(0)

