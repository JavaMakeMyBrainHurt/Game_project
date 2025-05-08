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
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 256, 256)
        self.flip = False
        self.speed = 15
        self.floor = y
        self.vel_y = 0
        self.jump_speed = -40
        self.jump = False
        self.attacking = False
        self.health = 100
        self.stagger_timer = 0
        self.attack_timer = 0
        self.attack_cooldown = 15
        self.attack_rect = None
        self.blocking = False
        self.block_duration = 30  # frames
        self.block_timer = 0

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        if self.attack_rect:
            pygame.draw.rect(screen, (0, 255, 0), self.attack_rect)
        if self.blocking:
            pygame.draw.rect(screen, (0, 0, 255), self.rect, 5)  # Blue border for blocking

    def attack(self, target):
        self.attacking = True
        self.attack_timer = self.attack_cooldown
        x = self.rect.centerx + 100 if not self.flip else self.rect.centerx - 100 - 180
        self.attack_rect = pygame.Rect(x, self.rect.top + 100, 180, 80)
        if self.attack_rect.colliderect(target.rect) and not target.blocking:
            target.health -= 10
            knockback = 100
            if self.flip:
                target.rect.x -= knockback
            else:
                target.rect.x += knockback
            target.stagger_timer = self.attack_cooldown

    def block(self):
        if not self.attacking and not self.blocking:
            self.blocking = True
            self.block_timer = self.block_duration

    def move(self, keys, left, right, jump, attack, target, block):
        vel_x = 0
        gravity = 4

        # Stagger
        if self.stagger_timer > 0:
            self.stagger_timer -= 1
            self.attacking = True
            return

        # Block duration logic
        if self.blocking:
            self.block_timer -= 1
            if self.block_timer <= 0:
                self.blocking = False
            return  # Skip other actions while blocking

        # Attack cooldown logic
        if self.attack_timer > 0:
            self.attack_timer -= 1
            self.attacking = True
        else:
            self.attacking = False
            self.attack_rect = None

        if not self.attacking:
            if keys[left]:
                vel_x -= self.speed
            if keys[right]:
                vel_x += self.speed
            if keys[jump] and not self.jump:
                self.vel_y = self.jump_speed
                self.jump = True
            self.vel_y += gravity
            self.rect.x += vel_x
            self.rect.y += self.vel_y
            if keys[attack]:
                self.attack(target)
            if keys[block]:
                self.block()

        # Screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= self.floor:
            self.rect.bottom = self.floor
            self.vel_y = 0
            self.jump = False

        # Flip check
        self.flip = target.rect.centerx < self.rect.centerx

player_1 = Player(200, 900)
player_2 = Player(1500, 900)

# Game loop
while run:
    clock.tick(60)
    bg_set()
    keys = pygame.key.get_pressed()

    player_1.move(keys, pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_r, player_2, pygame.K_t)
    player_2.move(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_KP1, player_1, pygame.K_KP2)

    player_1.draw()
    player_2.draw()

    draw_health_bar(player_1.health, 20, 20)
    draw_health_bar(player_2.health, 1500, 20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
