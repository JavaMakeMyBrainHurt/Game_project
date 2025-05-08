import pygame
pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
run = True
background = pygame.image.load('assets/background.png')
def bg_set():
    scale_bg = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scale_bg, (0, 0))
class Player:
    "Class for player object."
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 160, 360)
        self.speed = 15
        self.jump = False
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
    def move(self, keys, left, right, jump):
        if keys[left]:
            self.rect.x -= self.speed
        if keys[right]:
            self.rect.x += self.speed
        #inbounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        #jump
        if keys[jump] and self.jump == False:
player_1 = Player(200, 500)
player_2 = Player(1600, 500)
#game loop
while run:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    player_1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w)
    player_2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
    bg_set()
    player_1.draw()
    player_2.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
