"""
Apple Basket Environment
KeremCikikci -> keremcikikci@gmail.com
"""
from gym import Env
from gym.spaces import Discrete, Box

import numpy as np
import random

import pygame

showPanel = True

apples = []

WIDTH, HEIGHT = 400, 600
basketWidth, basketHeight = 30, 20

FPS = 120
APS = 4 # Apple Per Second
gravity = 4
basketSpeed = 10

terminate = 10 # Uncaught apple to terminate

# Initialize rendering requirements
pygame.init()
pygame.display.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Apple Basket")
clock = pygame.time.Clock()

class APPLE():
	def __init__(self):
		self.size = 10
		self.x = random.randint(0, WIDTH)
		self.y = 0

	def update(self):
		self.y += gravity

class AppleBasket(Env):
	"""
    ### Description
    This environment simulates an apple basket that collects falling apples by moving only horizontally.
    Field width and height, basket width and height, FPS, apples falling per second, gravity, and termination threshold variables 
    are fully adjustable from the top of the script.
    ### Action Space
    The action is a `ndarray` with shape `(1,)` which can take values `{0, 1, 2}` determines movement direction of the basket
    | Num | Action                       |
    |-----|------------------------------|
    | 0   | Move the basket to the left  |
    | 1   | hold the basket steady       |
    | 2   | Move the basket to the right |
    **Note**: The movement of the basket is not an accelerated movement, the position changes directly to the calculated place 
    corresponding to the basket speed.
    ### Observation Space
    The observation is a `ndarray` with shape `(3,)` with the values corresponding to the following positions:
    | Num | Observation                         | Min                 | Max               |
    |-----|-------------------------------------|---------------------|-------------------|
    | 0   | Basket Horizontall Position         | 0                   | Field Width       |
    | 1   | Closest Apple Horizontall Position  | 0                   | Field Width       |
    | 2   | Closest Apple Vertical Position     | 0                   | Field Height      |
    ### Rewards
    While a reward worth 1 is allocated for each apple caught, -1 value is lost in case of leaving the area.
    ### Starting State
    The horizontal position of the basket is set in the middle of the field and an apple is created in a random position.
    ### Episode End
    The episode ends if any one of the following occurs:
    1. Termination: The Basket cannot catch the defined number of apples
    2. Termination: The Basket leaves the area
    ### Additional Info
	Models trained in various steps are saved in the 'Saved Models' folder.
	The packages used in the environment can be installed by running the 'requirements.txt' file with the 'pip install -r requirements.txt' command.
    """

	def __init__(self):
		self.action_space = Discrete(3)
		self.observation_space = Box(np.array([0, 0, 0], dtype=int), np.array([WIDTH, WIDTH, HEIGHT], dtype=int), dtype=int) # agent_pos, closest apple pos
		self.agent_pos = [int(WIDTH / 2), HEIGHT - basketHeight]
		self.agent_size = [basketWidth, basketHeight]
		apples.append(APPLE())
		self.agentSpeed = basketSpeed
		self.frame = 0
		self.score = 0
		self.episode = 0
		self.missed = 0
		self.state = [int(self.agent_pos[0]), int(apples[0].x), int(apples[0].y)]

	def step(self, action):

		def detectCollision(apX, apY, apS, agP, agS):
			collision = False

			agTopLeft, agTopRight, agBottomLeft, agBottomRight = [agP[0] - agS[0], agP[1] - agS[1]], [agP[0] + agS[0], agP[1] - agS[1]], [agP[0] - agS[0], agP[1] + agS[1]], [agP[0] + agS[0], agP[1] + agS[1]]

			if (apX < agTopRight[0]) and (apX > agTopLeft[0]) and (apY > agTopLeft[1]) and (apY < agBottomLeft[1]):
				collision = True
			else:
				collision = False

			return collision

		self.frame += 1

		self.agent_pos[0] += self.agentSpeed if action == 2 else -self.agentSpeed if action == 0 else 0

		if self.frame%int(FPS/APS)==0:
			apples.append(APPLE())

		for apple in apples:
			apple.update()
			if apple.y >= HEIGHT:
				apples.remove(apple)
				self.missed += 1

		
		reward = int(detectCollision(apples[0].x, apples[0].y, apples[0].size, self.agent_pos, self.agent_size))
		if reward == 1:
			apples.remove(apples[0])
		if self.missed >= terminate or self.agent_pos[0] < 0 or self.agent_pos[0] > WIDTH:
			reward = -1
			done = True
		else:
			done = False

		self.score += reward

		info = {}

		self.state = [self.agent_pos[0], apples[0].x, apples[0].y]

		return self.state, reward, done, info



	def render(self, mode):
		window.fill((255, 255, 255))

		# Info Panel
		if showPanel:
			font = pygame.font.SysFont('consolas.ttf', 24)
			_episode = font.render('Episode: ' + str(self.episode), True, (0, 0, 0))
			window.blit(_episode, (10, 20))
			_score = font.render('Score: ' + str(self.score), True, (0, 0, 0))
			window.blit(_score, (110, 20))
			_missed = font.render('Missed: ' + str(self.missed), True, (0, 0, 0))
			window.blit(_missed, (205, 20))
			_FPS = font.render('FPS: ' + str(FPS), True, (84, 246, 48))
			window.blit(_FPS, (320, 20))
			_APS = font.render('Apple Per Second: ' + str(APS), True, (0, 0, 0))
			window.blit(_APS, (20, 40))
			_gravity = font.render('Gravity: ' + str(gravity), True, (0, 0, 0))
			window.blit(_gravity, (190, 40))

		for apple in apples:
			pygame.draw.circle(window, (255, 0, 0), [apple.x, apple.y], apple.size)

		pygame.draw.rect(window, (0, 0, 0), pygame.Rect(self.agent_pos[0], self.agent_pos[1], self.agent_size[0], self.agent_size[1]))	

		pygame.display.update()
		clock.tick(FPS)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

	def reset(self):
		self.agent_pos = [int(WIDTH / 2), HEIGHT - self.agent_size[1]]
		apples = []
		apples.append(APPLE())
		self.state = [self.agent_pos[0], apples[0].x, apples[0].y]
		self.score = 0
		self.episode += 1
		self.missed = 0

		return self.state
