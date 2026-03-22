import pygame, time
from core.config import *
from core.bird import Bird
from core.pipe import Pipe

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird AI")

        self.dt = 1.0 / UPS
        self.accumulator = 0.0
        self.last_time = time.perf_counter()
        
        # --- Entity Initalization ---
        self.bird = Bird(230, 350)
        self.pipes = [Pipe(600)]
        self.score = 0

        self.running = True
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    self.bird.jump()
                    
    def update(self, dt):
        self.bird.update()

        add_pipe = False
        rem = []

        for pipe in self.pipes:
            pipe.update()

            if not pipe.passed and pipe.x < self.bird.x:
                pipe.passed = True
                add_pipe = True
                
            if pipe.x + 52 < 0:
                rem.append(pipe)

        if add_pipe:
            self.score += 1
            self.pipes.append(Pipe(600))
        
        for r in rem:
            self.pipes.remove(r)
            
        if self.bird.y >= WINDOW_HEIGHT - 24 or self.bird.y < 0:
            self.bird.y = 350
    
    def draw(self, screen, alpha):
        self.screen.fill((135, 206, 235))
        # --- Draw entity ---
        for pipe in self.pipes:
            pipe.draw(screen, alpha)
            
        self.bird.draw(screen, alpha)
        # -------------------
        pygame.display.flip()

    def run(self):
        while self.running: 
            current_time = time.perf_counter()
            frame_time = current_time - self.last_time
            self.last_time = current_time
            
            if frame_time > 0.25:
                frame_time = 0.25
                
            self.accumulator += frame_time
            
            self.handle_events()

            while self.accumulator >= self.dt:
                self.update(self.dt)
                self.accumulator -= self.dt
                
            alpha = self.accumulator / self.dt
            
            self.draw(self.screen, alpha)
            
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()