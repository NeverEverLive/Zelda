import pygame, sys
import time

from settings import *
from level import Level


class Game:
	def __init__(self) -> None:
		pygame.init()
		pygame.display.set_caption('Zelda')

		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		self.clock = pygame.time.Clock()
		self.level = Level()

	def run(self) -> None:
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()
						return
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()

			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

			if self.level.restart:
				time.sleep(5)
				del self
				game = Game()
				game.run()

if __name__ == '__main__':
	game = Game()
	game.run()
