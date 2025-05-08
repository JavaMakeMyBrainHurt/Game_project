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
def draw_health_bar(health, x, y):
  ratio = health / 100
  pygame.draw.rect(screen, (255, 255, 255), (x - 2, y - 2, 404, 34))
  pygame.draw.rect(screen, (255, 0, 0), (x, y, 400, 30))
  pygame.draw.rect(screen, (255, 255, 0), (x, y, 400 * ratio, 30))

class Player:
    "Class for player object."

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 160, 360)
        self.flip = False
        self.speed = 15
        self.floor = y
        self.vel_y = 0
        self.jump_speed = -40
        self.jump = False
        self.attacking = False
        self.health = 100
        self.attack_cooldown = 0
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def attack(self, target):
        self.attacking = True
        attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y + 50 , 1.5 * self.rect.width, self.rect.height // 4)
        if attacking_rect.colliderect(target.rect):
            target.health -= 10
        pygame.draw.rect(screen, (0, 255, 0), attacking_rect)

    def move(self, keys, left, right, jump, attack, target):
        vel_x = 0
        gravity = 4

        if not self.attacking:  # ei saa midagi teha enne kui tegevus on lõppenud
            if keys[left]:
                vel_x -= self.speed
            if keys[right]:
                vel_x += self.speed

            # Jump
            if keys[jump] and not self.jump:
                self.vel_y = self.jump_speed
                self.jump = True

            self.vel_y += gravity
            self.rect.x += vel_x
            self.rect.y += self.vel_y

            # Attack
            if keys[attack]:
                self.attack(target)
        # Inbounds check
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= self.floor:
            self.rect.bottom = self.floor
            self.vel_y = 0
            self.jump = False
        #mängijad on vastakuti
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True



player_1 = Player(200, 900)
player_2 = Player(1500, 900)

# Game loop
while run:
    clock.tick(60)
    bg_set()
    keys = pygame.key.get_pressed()

    player_1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_r, player_2)
    player_2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_KP1, player_1)

    player_1.draw()
    player_2.draw()

    draw_health_bar(player_1.health, 20, 20)
    draw_health_bar(player_2.health, 1500, 20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
