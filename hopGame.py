

import pygame
import random
from settings import *
from hopSprites import *
from os import path

class Game:
    def __init__(self):
        #Initalize game window and other stuff
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = pygame.font.match_font(font_name)


    def new(self):
        # resets the game
        self.score = 0
        self.coinsamnt = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.LayeredUpdates()
        self.coins = pygame.sprite.LayeredUpdates()
        self.clouds = pygame.sprite.LayeredUpdates()
        self.player = Player(self)
        for plat in platform_list:
            Platform(self, *plat)

        Cloud(self, 0,0)
        Cloud(self, 0, -800)

        self.run()

    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.clock.tick(fps)
            self.events()
            self.update()
            self.draw()

    def update(self):
        #game loop - update
        self.all_sprites.update()


        #check if player hits a platform - only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player,self.platforms,False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit .rect.bottom > lowest.rect.bottom:
                        lowest = hit
                #first if is so you will fall off that platforms properly
                if self.player.pos.x < lowest.rect.right +10  and self.player.pos.x >lowest.rect.left -10:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top + 1
                        self.player.vel.y = 0
                        self.player.jumping = False

        #if player reaches top 1/4 of screen
        if self.player.rect.top <= height/4:
            for coin in self.coins:
                coin.rect.y += max(abs(self.player.vel.y),2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y),2)
                if plat.rect.top >= height:
                    plat.kill()
                    self.score += 10
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)


        #if player cloides with powerup
        coin_hits = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in coin_hits:
            self.coinsamnt += 1
            for coinn in self.coins:
                if coinn == coin:
                    coinn.kil()

        #If you fall
        if self.player.rect.bottom >height:
            for sprite in self.all_sprites:
                #takes the max number between ten and player velocity
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
                if len(self.platforms) == 0:
                    self.playing = False

        #spawn new platforms to keep the same average of platforms
        while len(self.platforms) <6:
            WIDTH = random.randrange(50,100)
            Platform(self,random.randrange(0,width-WIDTH),random.randrange(-75,-30))



    def events(self):
        #Game loop - events
        for event in pygame.event.get():
            # check for closing the window
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type ==pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
            if event.type ==pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        #game loop - draw
        self.screen.fill(bgcolour)
        self.all_sprites.draw(self.screen)
        self.draw_text(("Score: "+ str(self.score)), 22, black, 50, 15)
        self.draw_text(("Coins: "+ str(self.coinsamnt)), 22, black, 150, 15)
        # after drawing everything flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # games sttart screen
        self.screen.fill(bgcolour)
        self.draw_text(title, 48, black, width/2, height/4)
        self.draw_text("Arrows to move, Space to jump", 22, black, width/2, height/2)
        self.draw_text("Press a key to play", 22, black , width/2, height *3/4)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        # game over/continue
        if not self.running:
            return
        self.screen.fill(bgcolour)
        self.draw_text("GAME OVER", 48, black, width / 2, height / 4)
        self.draw_text("Score: " + str(self.score), 22, black, width / 2, height / 2)
        self.draw_text("Press a key to play again", 22, black, width / 2, height * 3 / 4)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, colour, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pygame.quit()
