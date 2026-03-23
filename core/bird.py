import pygame
from core.config import ROT_VEL
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.prev_y = y
        
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        
        self.image = pygame.Surface((34, 24))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def jump(self):
        self.vel = -ROT_VEL
        self.tick_count = 0
        self.height = self.y
        
    def update(self):
        self.prev_y = self.y
        self.tick_count += 1
        
        d = self.vel * self.tick_count + 1.0 * self.tick_count**2
        
        if d >= 12:
            d = 12
        if d < 0:
            d -= 2
            
        self.y = self.y + d
        
        self.rect.y = self.y
        
    def draw(self, screen, alpha):
        render_y = self.prev_y + (self.y - self.prev_y)

        render_rect = self.image.get_rect(topleft = (self.x, render_y))
        screen.blit(self.image, render_rect.topleft)