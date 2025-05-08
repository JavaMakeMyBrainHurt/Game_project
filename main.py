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
        self.floor = y
        self.vel_y = 0
        self.jump_speed = -40
        self.jump = False
        self.attacking = False
        self.health = 100
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
    def attack(self, keys):
        pass
    def move(self, keys, left, right, jump, attack, kick, block):
        vel_x = 0
        gravity = 4
        if keys[left]:
            vel_x -= self.speed
        if keys[right]:
            vel_x += self.speed
        #jump
        if keys[jump] and self.jump == False:
            self.vel_y = self.jump_speed
            self.jump = True
        self.vel_y += gravity
        self.rect.x += vel_x
        self.rect.y += self.vel_y
        #attack

        # inbounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= self.floor:
            self.rect.bottom = self.floor
            self.vel_y = 0
            self.jump = False

player_1 = Player(200, 900)
player_2 = Player(1600, 900)
#game loop
while run:
    clock.tick(60)
    keys = pygame.key.get_pressed()
    player_1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_r, pygame.K_t, pygame.K_y)
    player_2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_KP1, pygame.K_KP2, pygame.K_KP3)
    bg_set()
    player_1.draw()
    player_2.draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
