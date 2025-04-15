import pygame
from random import randint, uniform
from os.path import join

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 300
        
        # cooldown
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 400
        
        # mask
        self.mask = pygame.mask.from_surface(self.image)
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True
            
    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
        
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.right > WINDOW_WIDTH: self.rect.right = WINDOW_WIDTH
        if self.rect.bottom > WINDOW_HEIGHT: self.rect.bottom = WINDOW_HEIGHT
    
        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            
        self.laser_timer()
       
class Star(pygame.sprite.Sprite):
        def __init__(self, groups, surf):
            super().__init__(groups)
            self.image = surf
            self.rect = self.image.get_frect(center = (randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)))

class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        
    def update(self, dt):
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0: self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = self.original_surf
        self.rect = self.image.get_frect(center = pos)
        self.created_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = randint(400, 500)
        self.rotation = 0
        self.rotation_speed = randint(40, 80)
        
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        current_time = pygame.time.get_ticks()
        if current_time - self.created_time >= self.lifetime: self.kill()
        
        # continuous rotation
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_frect(center = self.rect.center)

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)
    
    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
             self.image = self.frames[int(self.frame_index)]
        else: self.kill()
        
def collisions():
    global running
    
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, False, pygame.sprite.collide_mask)
    if collision_sprites:
        running = False
    
    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            
def display_score():
    text_color = (240, 240, 240)
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(f'{current_time}', True, text_color)
    text_rect = text_surf.get_frect(midbottom = (WINDOW_WIDTH / 2, WINDOW_HEIGHT - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, text_color, text_rect.inflate(20, 16).move(0, -7), 5, 10)
    
# general setup
pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

# plain surface
surf = pygame.Surface((100, 200))
surf.fill('orange')
n_of_stars = 20
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
font = pygame.font.Font(join('images', 'Oxanium-Bold.ttf'), 40)
explosion_frames = [pygame.image.load(join('images', 'explosion', f'{i}.png')).convert_alpha() for i in range(21)]

star_surf = pygame.image.load(join('images', 'star.png')).convert_alpha()
meteor_surf = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
laser_surf = pygame.image.load(join('images', 'laser.png')).convert_alpha()

for i in range(n_of_stars):
    Star(all_sprites, star_surf)
player = Player(all_sprites)

# custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

while running:
    dt = clock.tick() / 1000

    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            pos = (randint(0, WINDOW_WIDTH), randint(-200, -100))
            Meteor(meteor_surf, pos, (all_sprites, meteor_sprites))
    
    # update
    all_sprites.update(dt)
    collisions()
        
    # draw the game
    display_surface.fill('#3a2e3f')
    display_score()  
    all_sprites.draw(display_surface)
    
    pygame.display.update()

pygame.quit()
