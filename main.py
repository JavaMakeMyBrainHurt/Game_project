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
def load_images(path, frame_count, scale_factor=4):
    images = []
    for i in range(1, frame_count + 1):
        img = pygame.image.load(f'{path}/frame_{i}.png').convert_alpha()
        width, height = img.get_size()
        scaled_img = pygame.transform.scale(img, (width * scale_factor, height * scale_factor))
        images.append(scaled_img)
    return images
sprite_run = load_images('assets/running_sprites', 12)
sprite_punch = load_images('assets/punch', 3)
sprite_block = load_images('assets/block', 2)

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 512, 512)
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
        self.block_duration = 30  # Block duration in frames
        self.block_timer = 0
        self.animations = {'run': sprite_run, 'attack': sprite_punch, 'block': sprite_block, 'idle': [sprite_run[0]]}
        self.current_action = 'idle'
        self.frame_index = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_speed = 100

    def set_action(self, new_action):
        if self.current_action != new_action:
            self.current_action = new_action
            self.frame_index = 0
            self.last_update = pygame.time.get_ticks()

    def draw(self):
        current_time = pygame.time.get_ticks()
        current_anim = self.animations[self.current_action]

        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            self.frame_index += 1
            if self.frame_index >= len(current_anim):
                self.frame_index = 0  # Loop

        frame = current_anim[self.frame_index]
        if self.flip:
            frame = pygame.transform.flip(frame, True, False)

        screen.blit(frame, self.rect.topleft)

        if self.attack_rect:
            pygame.draw.rect(screen, (0, 255, 0), self.attack_rect)
        if self.blocking:
            pygame.draw.rect(screen, (0, 0, 255), self.rect, 5)

    def attack(self, target):
        self.attacking = True
        self.attack_timer = self.attack_cooldown
        x = self.rect.centerx + 100 if not self.flip else self.rect.centerx - 100 - 180
        self.attack_rect = pygame.Rect(x + 100, self.rect.top + 300, 100, 80)
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

        if self.stagger_timer > 0:
            self.stagger_timer -= 1
            self.attacking = True
            return

        if self.blocking:
            self.block_timer -= 1
            if self.block_timer <= 0:
                self.blocking = False

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

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom >= self.floor:
            self.rect.bottom = self.floor
            self.vel_y = 0
            self.jump = False

        if self.attacking:
            self.set_action('attack')
        elif self.blocking:
            self.set_action('block')
        elif keys[left] or keys[right]:
            self.set_action('run')
        else:
            self.set_action('idle')  # Use idle action when not moving or attacking

        self.flip = target.rect.centerx < self.rect.centerx
player_1 = Player(200, 900)
player_2 = Player(1500, 900)

#loop
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
        if event.type == pygame.QUIT or player_2.health <= 0 or player_1.health <= 0:
            run = False

    pygame.display.update()

pygame.quit()
