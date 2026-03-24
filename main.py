import pygame
import time
import neat
import os
import sys

from core.config import *
from core.bird import Bird
from core.pipe import Pipe
from core.base import Base

# --- KHỐI 1: CHẾ ĐỘ NGƯỜI CHƠI (MANUAL) ---
class FlappyManual:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.SysFont("comicsansms", 40, bold=True)
        self.small_font = pygame.font.SysFont("comicsansms", 20)
        self.dt = 1.0 / UPS
        self.state = STATE_MENU
        self.running = True
        self.exit_to_menu = False # Trả về Main Menu tổng
        self.reset_game()

    def reset_game(self):
        self.bird = Bird(150, 350)
        self.pipes = [Pipe(500)]
        self.base = Base(WINDOW_HEIGHT - 100)
        self.score = 0

    def play(self):
        accumulator = 0.0
        last_time = time.perf_counter()

        while self.running and not self.exit_to_menu:
            current_time = time.perf_counter()
            frame_time = current_time - last_time
            last_time = current_time

            if frame_time > 0.25: frame_time = 0.25
            accumulator += frame_time
            
            # --- EVENTS ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Quay lại Main Menu
                        self.exit_to_menu = True
                    if event.key == pygame.K_SPACE:
                        if self.state == STATE_MENU: self.state = STATE_PLAYING; self.bird.jump()
                        elif self.state == STATE_PLAYING: self.bird.jump()
                        elif self.state == STATE_GAMEOVER: self.reset_game(); self.state = STATE_PLAYING; self.bird.jump()

            # --- UPDATE ---
            while accumulator >= self.dt:
                if self.state == STATE_PLAYING:
                    self.bird.update()
                    self.base.update()
                    add_pipe = False
                    rem = []
                    
                    for pipe in self.pipes:
                        pipe.update()
                        if pipe.collide(self.bird): self.state = STATE_GAMEOVER
                        if not pipe.passed and pipe.x + pipe.PIPE_TOP.get_width() < self.bird.x:
                            pipe.passed = True; add_pipe = True
                        if pipe.x + pipe.PIPE_TOP.get_width() < 0: rem.append(pipe)
                            
                    if add_pipe: self.score += 1; self.pipes.append(Pipe(500))
                    for r in rem: self.pipes.remove(r)
                        
                    if self.bird.y >= self.base.y - self.bird.image.get_height() or self.bird.y < 0:
                        self.state = STATE_GAMEOVER
                
                accumulator -= self.dt

            # --- DRAW ---
            alpha = accumulator / self.dt if self.state == STATE_PLAYING else 1.0
            
            self.screen.fill((135, 206, 235))
            for pipe in self.pipes: pipe.draw(self.screen, alpha)
            self.base.draw(self.screen, alpha)
            self.bird.draw(self.screen, alpha)
            
            if self.state in [STATE_PLAYING, STATE_GAMEOVER]:
                score_text = self.font.render(str(self.score), True, (255, 255, 255))
                self.screen.blit(score_text, (WINDOW_WIDTH//2 - score_text.get_width()//2, 50))
            if self.state == STATE_MENU:
                t = self.small_font.render("Press SPACE to Start", True, (255, 255, 255))
                self.screen.blit(t, (WINDOW_WIDTH//2 - t.get_width()//2, WINDOW_HEIGHT//2))
            if self.state == STATE_GAMEOVER:
                t = self.small_font.render("GAME OVER - Press SPACE to Retry", True, (255, 0, 0))
                self.screen.blit(t, (WINDOW_WIDTH//2 - t.get_width()//2, WINDOW_HEIGHT//2))
                
            pygame.display.flip()


# --- KHỐI 2: CHẾ ĐỘ AI (NEAT) ---
class FlappyAI:
    def __init__(self, genomes, config, gen_count):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.SysFont("comicsansms", 40, bold=True)
        self.small_font = pygame.font.SysFont("comicsansms", 20)
        self.dt = 1.0 / UPS
        self.gen = gen_count
        
        self.birds, self.nets, self.ge = [], [], []
        for _, g in genomes:
            net = neat.nn.FeedForwardNetwork.create(g, config)
            self.nets.append(net); self.birds.append(Bird(150, 350))
            g.fitness = 0; self.ge.append(g)

        self.pipes = [Pipe(500)]
        self.base = Base(WINDOW_HEIGHT - 100)
        self.score = 0
        self.running = True
        self.exit_to_menu = False

    def remove_bird(self, index):
        self.birds.pop(index); self.nets.pop(index); self.ge.pop(index)

    def play(self):
        accumulator = 0.0
        last_time = time.perf_counter()

        while self.running and len(self.birds) > 0 and not self.exit_to_menu:
            current_time = time.perf_counter()
            frame_time = current_time - last_time
            last_time = current_time
            if frame_time > 0.25: frame_time = 0.25
            accumulator += frame_time
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.exit_to_menu = True # Thoát khỏi đánh giá AI để về Main Menu
                    return

            while accumulator >= self.dt:
                self.base.update()
                pipe_ind = 0
                if len(self.birds) > 0:
                    if len(self.pipes) > 1 and self.birds[0].x > self.pipes[0].x + self.pipes[0].PIPE_TOP.get_width():
                        pipe_ind = 1
                else: 
                    self.running = False; break
                
                for x, bird in enumerate(self.birds):
                    bird.update()
                    self.ge[x].fitness += 0.1
                    input_data = (bird.y, abs(bird.y - self.pipes[pipe_ind].top), abs(bird.y - self.pipes[pipe_ind].bottom))
                    if self.nets[x].activate(input_data)[0] > 0.5:
                        bird.jump()

                add_pipe = False
                rem = []
                for pipe in self.pipes:
                    pipe.update()
                    for x, bird in enumerate(self.birds):
                        if pipe.collide(bird):
                            self.ge[x].fitness -= 1
                            self.remove_bird(x)
                    if len(self.birds) > 0 and not pipe.passed and pipe.x + pipe.PIPE_TOP.get_width() < self.birds[0].x:
                        pipe.passed = True; add_pipe = True
                    if pipe.x + pipe.PIPE_TOP.get_width() < 0: rem.append(pipe)

                if add_pipe:
                    self.score += 1
                    for g in self.ge: g.fitness += 5
                    self.pipes.append(Pipe(500))
                    
                for r in rem: self.pipes.remove(r)

                for x, bird in enumerate(self.birds):
                    if bird.y >= self.base.y - bird.image.get_height() or bird.y < 0:
                        self.remove_bird(x)
                        
                accumulator -= self.dt

            alpha = accumulator / self.dt
            self.screen.fill((135, 206, 235))
            for pipe in self.pipes: pipe.draw(self.screen, alpha)
            self.base.draw(self.screen, alpha)
            for bird in self.birds: bird.draw(self.screen, alpha)
            
            s_text = self.font.render(f"{self.score}", True, (255, 255, 255))
            i_text = self.small_font.render(f"Gen: {self.gen} | Alive: {len(self.birds)}", True, (0, 0, 0))
            self.screen.blit(s_text, (WINDOW_WIDTH//2 - s_text.get_width()//2, 20))
            self.screen.blit(i_text, (10, 10))
            pygame.display.flip()

# Biến global đếm Generation và cờ thoát cho AI
GENERATION = 0
FORCE_QUIT_AI = False

def eval_genomes(genomes, config):
    global GENERATION, FORCE_QUIT_AI
    if FORCE_QUIT_AI: return # Nếu người dùng ấn ESC, ngừng huấn luyện
    GENERATION += 1
    game = FlappyAI(genomes, config, GENERATION)
    game.play()
    if game.exit_to_menu:
        FORCE_QUIT_AI = True


# --- KHỐI 3: TRÌNH ĐIỀU KHIỂN CHÍNH (MAIN CONTROLLER) ---
def run_game():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Flappy Bird: Portfolio Project")
    font = pygame.font.SysFont("comicsansms", 30, bold=True)
    small_font = pygame.font.SysFont("comicsansms", 20)
    
    global FORCE_QUIT_AI, GENERATION
    
    while True:
        screen.fill((135, 206, 235))
        title = font.render("FLAPPY BIRD AI", True, (255, 255, 255))
        op1 = small_font.render("[ 1 ] Manual Mode", True, (0, 0, 0))
        op2 = small_font.render("[ 2 ] AI Mode (NEAT)", True, (0, 0, 0))
        
        screen.blit(title, (WINDOW_WIDTH//2 - title.get_width()//2, 150))
        screen.blit(op1, (WINDOW_WIDTH//2 - op1.get_width()//2, 300))
        screen.blit(op2, (WINDOW_WIDTH//2 - op2.get_width()//2, 350))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    # PLAY MANUAL
                    manual_game = FlappyManual()
                    manual_game.play()

                elif event.key == pygame.K_2:
                    # PLAY AI
                    FORCE_QUIT_AI = False
                    GENERATION = 0
                    local_dir = os.path.dirname(__file__)
                    config_path = os.path.join(local_dir, "config-feedforward.txt")
                    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
                    p = neat.Population(config)
                    p.run(eval_genomes, 50)

if __name__ == "__main__":
    run_game()