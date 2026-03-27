import pygame
import random
import sys

pygame.init()


WIDTH, HEIGHT = 800, 400
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
DARK_GREY = (50, 50, 50)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Jump Offline")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, True)

class Dino:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT - 60
        self.vel_y = 0
        self.jumping = False

    def jump(self):
        if not self.jumping:
            self.vel_y = -15
            self.jumping = True

    def update(self):
        self.y += self.vel_y
        if self.jumping:
            self.vel_y += 0.8
        if self.y >= HEIGHT - 60:
            self.y = HEIGHT - 60
            self.jumping = False

    def draw(self):
        pygame.draw.rect(screen, DARK_GREY, (self.x, self.y, 40, 40))

class Cactus:
    def __init__(self):
        self.x = WIDTH + random.randint(100, 500)
        self.y = HEIGHT - 50
        self.width = 20
        self.height = 40

    def update(self, speed):
        self.x -= speed

    def draw(self):
        pygame.draw.rect(screen, GREY, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, GREY, (self.x - 5, self.y + 10, 5, 15))
        pygame.draw.rect(screen, GREY, (self.x + self.width, self.y + 15, 5, 15))

def main():
    dino = Dino()
    obstacles = [Cactus()]
    score = 0
    speed = 7
    run = True

    while run:
        screen.fill(WHITE)
        score += 0.1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()

        dino.update()
        
        if obstacles[-1].x < WIDTH - 300:
            obstacles.append(Cactus())

        for obs in obstacles[:]:
            obs.update(speed)
            if obs.x < -obs.width:
                obstacles.remove(obs)
            
            # Коллизия
            dino_rect = pygame.Rect(dino.x, dino.y, 40, 40)
            obs_rect = pygame.Rect(obs.x, obs.y, obs.width, obs.height)
            if dino_rect.colliderect(obs_rect):
                run = False 
        pygame.draw.line(screen, GREY, (0, HEIGHT-20), (WIDTH, HEIGHT-20), 2)
        dino.draw()
        for obs in obstacles:
            obs.draw()
        
        score_txt = font.render(f"Score: {int(score)}", True, DARK_GREY)
        screen.blit(score_txt, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)
    
    main() 
if __name__ == "__main__":
    main()