import pygame, random
from core.config import GAP, VEL

class Pipe:
    def __init__(self, x):
        self.x = x
        self.prev_x = x
        self.height = 0
        
        self.top = 0
        self.bottom = 0
        
        self.PIPE_TOP = pygame.Surface((52, 600))
        self.PIPE_TOP.fill((0, 255, 0))
        self.PIPE_BOTTOM = pygame.Surface((52, 600))
        self.PIPE_BOTTOM.fill((0, 255, 0))

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + GAP
        
    def update(self):
        self.prev_x = self.x
        self.x -= VEL
        
    def draw(self, screen, alpha):
        render_x = self.prev_x + (self.x - self.prev_x)

        screen.blit(self.PIPE_TOP,(render_x, self.top))
        screen.blit(self.PIPE_BOTTOM, (render_x, self.bottom))

    def get_rects(self):
        top_rect = pygame.Rect(self.x, self.top, self.PIPE_TOP.get_width(), self.PIPE_TOP.get_height())
        bottom_rect = pygame.Rect(self.x, self.bottom, self.PIPE_BOTTOM.get_width(), self.PIPE_BOTTOM.get_height())
        return top_rect, bottom_rect

    def collide(self, bird):
        bird_rect = bird.image.get_rect(topleft = (bird.x, bird.y))
        top_rect, bottom_rect = self.get_rects()

        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            return True
        return False