import pygame
from random import choice, randrange
from settings import *
vec = pygame.math.Vector2



class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        self._layer = player_layer
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game #so it knows about what is in the game
        self.walking = False
        self.jumping = False
        self.current_frame= 0
        self.last_update = 0
        self.load_images()
        self.image = self.imageright
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        self.pos = vec(40, height-100)
        self.vel = vec(0,0)
        self.acc = vec(0,0)

    def load_images(self):
        self.imageright = pygame.image.load('pig.png')
        self.imageright = pygame.transform.scale(self.imageright, (80,80))
        self.imageright.set_colorkey(black)

        self.imageleft = pygame.image.load('pig left.png')
        self.imageleft = pygame.transform.scale(self.imageleft, (80, 80))
        self.imageleft.set_colorkey(black)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        #jump only is standing on a platform
        self.rect.x += 2
        #if I change it to True then the blaocks will dispaear after you jump on it
        hits = pygame.sprite.spritecollide(self,self.game.platforms, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -player_jump

    def update(self):
        self.animate()
        self.acc = vec(0,player_grav)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.acc.x = -player_acc
        if keys[pygame.K_RIGHT]:
            self.acc.x = player_acc

        #applies to friction
        self.acc.x += self.vel.x * player_friction
        #equation of motion
        self.vel += self.acc
        if abs(self.vel.x) <0.1:
            self.vel.x = 0
        self.pos += self.vel + 0.5 * self.acc
        #wrap around the sides of the screen
        if self.pos.x > width + self.rect.width/2:
            self.pos.x = 0 - self.rect.width/2
        if self.pos.x < 0 - self.rect.width/2:
            self.pos.x = width +self.rect.width/2


    def animate(self):
        now = pygame.time.get_ticks()
        if self.vel.x != 0:
            walking = True
        else:
            walking = False
        #code to show walk animation
        if walking:
            if now-self.last_update >200:
                self.last_update = now
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.imageright
                else:
                    self.image=self.imageleft
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                bottom = self.rect.bottom
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.rect.midbottom = self.pos
        self.mask = pygame.mask.from_surface(self.image)

class Cloud(pygame.sprite.Sprite):
    def __init__ (self,game, x,y):
        self._layer = cloud_layer
        self.groups = game.all_sprites, game.clouds
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('clouds.png')
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale (self.image,(800,800))
        self.rect.x = x
        self.rect.y = y


    def update(self):
        if self.rect.y >= 600:
            self.rect.y = -1000

class Platform(pygame.sprite.Sprite):
    def __init__ (self,game,x,y):
        self._layer = platform_layer
        self.groups = game.all_sprites, game.platforms
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load('platforms.png')
        self.image = pygame.transform.scale(self.image, (200, 40))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < 10:
            Coin(self.game,self)

class Coin(pygame.sprite.Sprite):
    def __init__ (self,game,plat):
        self._layer = coin_layer
        self.groups = game.all_sprites,game.coins
        pygame.sprite.Sprite.__init__(self,self.groups)
        self.game = game
        self.plat = plat
        self.image = pygame.image.load('coin.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()