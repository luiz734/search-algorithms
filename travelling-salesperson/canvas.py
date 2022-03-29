import pygame
from pygame.locals import *

class Canvas:
   RED = (255, 0, 0)
   BLUE = (0, 0, 255)
   BLACK = (0, 0, 0)
   WHITE = (255, 255, 255)

   def __init__(self, height, width, scale) -> None: 
      self.DISPLAYSURF = pygame.display.set_mode((height * scale, width * scale))
      self.DISPLAYSURF.fill(Canvas.WHITE)
      self.scale = scale

      pygame.font.init()
      self.font = pygame.font.SysFont('Comic Sans MS', 16)

      pygame.init()
      pygame.event.get()

   def draw(self, points, connections, fields=[]):
      self.DISPLAYSURF.fill(Canvas.WHITE)
      for p in points: 
         idx = points.index(p) # nice
         pygame.draw.circle(self.DISPLAYSURF, self.BLACK, [self.scale * x for x in p], 5)
         # self.draw_text([10 + self.scale * x for x in p], [str(chr(65+idx)), "aa"])

      for i in range(len(connections)):
         pointa_a = (self.scale * points[connections[i % len(connections)]][0], self.scale * points[connections[i % len(connections)]][1])
         pointa_b = (self.scale * points[connections[(i + 1) % len(connections)]][0], self.scale * points[connections[(i + 1) % len(connections)]][1])
         pygame.draw.line(self.DISPLAYSURF, self.RED, pointa_a, pointa_b, 3)

      start_pos = [0 * self.scale, 0]
      spacement = 16
      for f in fields:
         img = self.font.render(f, True, Canvas.BLUE)
         self.DISPLAYSURF.blit(img, start_pos)     
         start_pos[1] += spacement

      pygame.display.update()
   
   def get_events(self):
      pygame.event.get()
