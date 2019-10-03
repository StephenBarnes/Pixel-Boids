#!/usr/bin/env python2

from pygame_framework import *
import random
import IPython

SCREEN_SHAPE = np.asarray((800,1000))


# For flocking behavior
if False:
	NUM_BOIDS = 50
	INFLUENCING_RADIUS = 36
	DISPERSION_RADIUS = 18
	FRICTION_BASE = .92
	RANDOM_MOVEMENT_SIZE = .4
	ALIGNMENT_STRENGTH = .3
	NON_ALIGNED_DECAY = 1 - ALIGNMENT_STRENGTH
	COHESION_STRENGTH = .03
	DISPERSION_STRENGTH = .1
# For bonding and chaotic swarming
if True:
	NUM_BOIDS = 50
	INFLUENCING_RADIUS = 60
	DISPERSION_RADIUS = 30
	FRICTION_BASE = .8
	RANDOM_MOVEMENT_SIZE = .01
	ALIGNMENT_STRENGTH = -.05
	NON_ALIGNED_DECAY = 1.
	COHESION_STRENGTH = .3
	DISPERSION_STRENGTH = .4


class Boid(BlockedNewtonianPixel):
	def update_velocity(self, pressed, game_state):
		self.velocity += np.random.randn(2) * RANDOM_MOVEMENT_SIZE
		self.velocity *= FRICTION_BASE

		influencing_boids = []
		for other_boid in game_state.object_collection.objects:
			dist = self.distance_to(other_boid, game_state)
			if dist < INFLUENCING_RADIUS:
				influencing_boids.append((dist, other_boid))

		# Alignment
		if influencing_boids:
			self.velocity *= NON_ALIGNED_DECAY
			for dist, b in influencing_boids:
				self.velocity += ALIGNMENT_STRENGTH * b.velocity / float(len(influencing_boids))

		# Cohesion
		if influencing_boids:
			center_of_mass = sum((b.pos for d, b in influencing_boids), np.zeros(2)) / float(len(influencing_boids))
			displacement = self.pos - center_of_mass
			self.velocity += -COHESION_STRENGTH * displacement

		# Dispersion
		for dist, b in influencing_boids:
			if dist < DISPERSION_RADIUS:
				displacement = self.pos - b.pos
				self.velocity += DISPERSION_STRENGTH * displacement

		# Apply sigmoid to velocity magnitude
		#old_magnitude = norm(self.velocity)
		#new_magnitude = 3 * logistic(old_magnitude)
		#self.velocity /= old_magnitude
		#self.velocity *= new_magnitude

class BoidCollection(ObjectCollection):
	object_type = Boid

class BoidState(ObjectCollectionGameState):
	object_collection_class = BoidCollection

class PixelBoidsGame(Game):
    pass


try:
	game = PixelBoidsGame(screen_shape=SCREEN_SHAPE, verbose=False)
	state = BoidState(game, num_objects=NUM_BOIDS)
	game.state = state
	game.run()
except Exception as e:
	print e
	print
	IPython.embed()

