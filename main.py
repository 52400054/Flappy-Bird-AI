import pygame, time
from core.config import *
from core.bird import Bird
from core.pipe import Pipe
from core.base import Base

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Flappy Bird AI")
        
        self.font = pygame.font.SysFont(None, 40, bold=True)
        self.small_font = pygame.font.SysFont(None, 20)

        self.dt = 1.0 / UPS
        self.accumulator = 0.0
        self.last_time = time.perf_counter()
        
        # --- Entity Initalization ---
        self.state = STATE_MENU
        self.running = True
        
        self.reset_game()
        
    def reset_game(self):
        self.bird = Bird(150, 350)
        self.pipes = [Pipe(500)]
        self.base = Base(WINDOW_HEIGHT - 100)
        self.score = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_SPACE:
                    if self.state == STATE_MENU:
                        self.state = STATE_PLAYING
                        self.bird.jump()
                    elif self.state == STATE_PLAYING:
                        self.bird.jump()
                    elif self.state == STATE_GAMEOVER:
                        self.reset_game()
                        self.state = STATE_PLAYING
                        self.bird.jump()


    def update(self, dt):
        if self.state != STATE_PLAYING:
            return
        
        self.bird.update()
        self.base.update()

        add_pipe = False
        rem = []

        for pipe in self.pipes:
            pipe.update()
            
            if pipe.collide(self.bird):
                self.state = STATE_GAMEOVER

            if not pipe.passed and pipe.x + pipe.PIPE_TOP.get_width() < self.bird.x:
                pipe.passed = True
                add_pipe = True
                
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

        if add_pipe:
            self.score += 1
            self.pipes.append(Pipe(500))
        
        for r in rem:
            self.pipes.remove(r)
            
        if self.bird.y >= self.base.y - self.bird.image.get_height() or self.bird.y < 0:
            self.state = STATE_GAMEOVER
    
    def draw(self, screen, alpha):
        self.screen.fill((135, 206, 235))
        # --- Draw entity ---
        for pipe in self.pipes:
            pipe.draw(screen, alpha)

        self.base.draw(screen, alpha)
        self.bird.draw(screen, alpha)
        # -------------------
        
        # --- Draw UI ---
        if self.state == STATE_PLAYING or self.state == STATE_GAMEOVER:
            score_text = self.font.render(str(self.score), True, (255, 255, 255))
            self.screen.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, 50))
            
        if self.state == STATE_MENU:
            text = self.small_font.render("Press SPACE to Start", True, (255, 255, 255))
            self.screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2))
            
        if self.state == STATE_GAMEOVER:
            text = self.small_font.render("GAME OVER - Press SPACE to Retry", True, (255, 0, 0))
            self.screen.blit(text, (WINDOW_WIDTH//2 - text.get_width()//2, WINDOW_HEIGHT//2))
        # ---------------
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
                
            alpha = self.accumulator / self.dt if self.state == STATE_PLAYING else 1.0
            
            self.draw(self.screen, alpha)
            
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()