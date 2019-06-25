import pygame
import os
import math



class Game:
  def __init__(self):
    self.screen_size = self.width, self.height = 800, 800
    self.screen = pygame.display.set_mode(self.screen_size)

  def run(self):
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_q):
          running = False
      
      self.screen.fill(BLACK)
      pygame.display.flip()

def main():
  pygame.init()
  game = Game()
  game.run()

if __name__ == '__main__':
  main()