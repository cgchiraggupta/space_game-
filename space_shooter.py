import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill(CYAN)
        # Draw a simple ship shape
        pygame.draw.polygon(self.image, WHITE, [(40, 15), (0, 0), (0, 30)])
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.speed = 5
        self.health = 100
        self.shoot_delay = 250  # milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep player on screen
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 5))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 10

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        pygame.draw.polygon(self.image, ORANGE, [(0, 15), (30, 0), (30, 30)])
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = random.randint(20, 50)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, (100, 100, 100), (self.size//2, self.size//2), self.size//2)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(0, 200)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(1, 3)
        self.rotation = 0
        self.rotation_speed = random.randint(-5, 5)

    def update(self):
        self.rect.x -= self.speed
        self.rotation += self.rotation_speed
        if self.rect.right < 0:
            self.kill()

# Star class for background
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 2))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(0.5, 2)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randint(0, HEIGHT)

# Explosion effect
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.images = []
        for i in range(10):
            img = pygame.Surface((40 + i * 4, 40 + i * 4))
            img.fill(BLACK)
            pygame.draw.circle(img, YELLOW if i < 5 else ORANGE, 
                             (20 + i * 2, 20 + i * 2), 20 + i * 2)
            img.set_colorkey(BLACK)
            self.images.append(img)
        self.current_frame = 0
        self.image = self.images[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.current_frame += 1
            if self.current_frame >= len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.images[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLACK)
        pygame.draw.circle(self.image, GREEN, (10, 10), 10)
        pygame.draw.circle(self.image, WHITE, (10, 10), 5)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Sprite groups
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
stars = pygame.sprite.Group()
explosions = pygame.sprite.Group()
powerups = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create background stars
for _ in range(100):
    star = Star()
    all_sprites.add(star)
    stars.add(star)

# Game variables
score = 0
game_over = False
spawn_timer = 0
powerup_timer = 0

# Font
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Game loop
running = True
while running:
    clock.tick(FPS)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.shoot()
            if event.key == pygame.K_r and game_over:
                # Restart game
                game_over = False
                score = 0
                player.health = 100
                player.rect.center = (100, HEIGHT // 2)
                
                # Clear all sprites except stars
                for sprite in all_sprites:
                    if sprite not in stars and sprite != player:
                        sprite.kill()
                
                enemies.empty()
                asteroids.empty()
                bullets.empty()
                explosions.empty()
                powerups.empty()

    if not game_over:
        # Continuous shooting when holding space
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()

        # Spawn enemies and asteroids
        spawn_timer += 1
        if spawn_timer > 60:  # Spawn every second
            spawn_timer = 0
            if random.random() > 0.5:
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
            else:
                asteroid = Asteroid()
                all_sprites.add(asteroid)
                asteroids.add(asteroid)

        # Spawn power-ups occasionally
        powerup_timer += 1
        if powerup_timer > 600:  # Every 10 seconds
            powerup_timer = 0
            if random.random() > 0.7:
                powerup = PowerUp()
                all_sprites.add(powerup)
                powerups.add(powerup)

        # Update sprites
        all_sprites.update()

        # Check bullet collisions with enemies
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 10
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)

        # Check bullet collisions with asteroids
        hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in hits:
            score += 5
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)

        # Check player collisions with enemies
        hits = pygame.sprite.spritecollide(player, enemies, True)
        for hit in hits:
            player.health -= 20
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)

        # Check player collisions with asteroids
        hits = pygame.sprite.spritecollide(player, asteroids, True)
        for hit in hits:
            player.health -= 15
            explosion = Explosion(hit.rect.centerx, hit.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)

        # Check player collisions with power-ups
        hits = pygame.sprite.spritecollide(player, powerups, True)
        for hit in hits:
            player.health = min(100, player.health + 20)
            score += 15

        # Check if player is dead
        if player.health <= 0:
            game_over = True
            explosion = Explosion(player.rect.centerx, player.rect.centery)
            all_sprites.add(explosion)
            explosions.add(explosion)

    # Drawing
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw HUD
    if not game_over:
        # Score
        score_text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_text, (10, 10))

        # Health bar
        health_text = small_font.render('Health:', True, WHITE)
        screen.blit(health_text, (10, 50))
        health_bar_width = 200
        health_bar_height = 20
        pygame.draw.rect(screen, RED, (10, 75, health_bar_width, health_bar_height))
        pygame.draw.rect(screen, GREEN, (10, 75, health_bar_width * (player.health / 100), health_bar_height))
        pygame.draw.rect(screen, WHITE, (10, 75, health_bar_width, health_bar_height), 2)

        # Controls
        controls_text = small_font.render('WASD/Arrows: Move | SPACE: Shoot', True, WHITE)
        screen.blit(controls_text, (WIDTH - 350, 10))
    else:
        # Game Over screen
        game_over_text = font.render('GAME OVER', True, RED)
        score_text = font.render(f'Final Score: {score}', True, WHITE)
        restart_text = small_font.render('Press R to Restart', True, WHITE)
        
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

pygame.quit()
