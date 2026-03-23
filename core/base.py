import pygame
from core.config import VEL, WIDTH

class Base:
    def __init__(self, y):
        self.y = y
        self.x = 0
        self.prev_x = 0
        
        self.image = pygame.Surface((WIDTH * 2, 100))
        self.image.fill((139, 69, 19))

    def update(self):
        self.prev_x = self.x
        self.x -= VEL
        if self.x <= -WIDTH:
            self.x = 0
            self.prev_x = self.prev_x + WIDTH
            
    def draw(self, screen, alpha):
        render_x = self.prev_x + (self.x - self.prev_x)
        screen.blit(self.image, (render_x, self.y))