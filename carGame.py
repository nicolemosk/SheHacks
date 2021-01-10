import pygame
import time
import random
from settings import *

bg = (156,167,188)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width,height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = True

    def new(self):

        self.car_width = 80
        self.carImg = pygame.image.load('car.png')
        self.carImg = pygame.transform.scale(self.carImg, (80, 160))
        self.x = (width * 0.45)
        self.y = (height * 0.7)

        self.x_change = 0

        self.coinx = random.randrange(0, width)
        self.coiny = -300
        self.holder = False

        self.thing_startx = random.randrange(0, width)
        self.thing_starty = -600
        self.thing_speed = 5
        self.thing_width = 100
        self.thing_height = 100
        self.idk = random.randint(1,2)

        self.dodged = 0
        self.coinsamnt = 0

        self.yy = [600,500,400,300,200,100,0,-100,-200,-300]
        for y in self.yy:
            Stripe(self.screen, y)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.x_change = -5
                elif event.key == pygame.K_RIGHT:
                    self.x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.x_change = 0

        self.x += self.x_change

        self.screen.fill(bg)
        for y in range(len(self.yy)):
            self.yy[y] += self.thing_speed
            Stripe(self.screen,self.yy[y])
            if self.yy[y] > 700:
                self.yy[y] = -300



        self.things(self.thing_startx, self.thing_starty, self.thing_width, self.thing_height, black)
        Coin(self.screen, self.coinx, self.coiny)



        self.thing_starty += self.thing_speed
        self.coiny += self.thing_speed

        self.car(self.x,self.y)


        if self.x > width - self.car_width or self.x < 0:
            self.playing = False

        if self.thing_starty > height:
            self.thing_starty = 0 - self.thing_height
            self.thing_startx = random.randrange(0,width)
            self.dodged += 1
            self.thing_speed +=1
            self.thing_width +=(self.dodged * 0.2)


        if self.y <self.coiny:
            if self.x > self.coinx -20 and self.x < self.coinx + 20:
                self.holder = True
            elif self.x + self.car_width > self.coinx - 20 and self.x + self.car_width < self.coinx + 20:
                self.holder = True


        if self.coiny > height or self.holder == True:
            self.coiny = 0 - self.thing_height
            self.coinx = random.randrange(0, width)
            self.idk = random.randint(1, 2)
            if self.holder:
                self.holder = False
                self.coinsamnt += 1

        if self.y < self.thing_starty + self.thing_height:
            if self.x > self.thing_startx and self.x < self.thing_startx + self.thing_width:
                self.playing = False
            elif self.x + self.car_width > self.thing_startx and self.x + self.car_width < self.thing_startx + self.thing_width:
                self.playing = False

        self.draw_text(("Score: " + str(self.dodged)), 22, black, 50, 15)
        self.draw_text(("Coins: " + str(self.coinsamnt)), 22, black, 150, 15)

        pygame.display.update()

        self.clock.tick(60)

    def run(self):
        self.playing = True
        while self.playing:
            self.update()

    def draw_text(self, text, size, colour, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.screen.blit(text_surface, text_rect)

    def things_dodged(self,count):
        self.font = pygame.font.SysFont(None, 25)
        self.text = self.font.render("Dodged: " + str(count), True, red)
        self.screen.blit(self.text, (0, 0))

    def coins_collected(self,count):
        self.font = pygame.font.SysFont(None, 25)
        self.text = self.font.render("Coins: " + str(count), True, red)
        self.screen.blit(self.text, (100, 0))

    def things(self,thingx, thingy, thingw, thingh, colour):
        self.image1 = pygame.image.load('log.png')
        self.image1 = pygame.transform.scale(self.image1, (100, 50))
        self.image1.set_colorkey(white)
        self.screen.blit(self.image1, (thingx, thingy))


    def car(self,x, y):
        self.screen.blit(self.carImg, (x, y))

    def text_objects(self,text, font):
        self.textSurface = self.font.render(text, True, black)
        return self.textSurface, self.textSurface.get_rect()

    # game_loop()
    def draw_text(self, text, size, colour, x, y):  # function that makes it less lines to draw text
        myfont = pygame.font.SysFont('arial', size)  # here is where it sets the font and size
        text_surface = myfont.render(text, True, colour)  # here it sets the colour
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)  # here it sets the position
        self.screen.blit(text_surface, text_rect)  # here it puts it onto the screen

    def show_go_screen(self): #this is for the gameover screen
        if not self.running: #if self.running = false than that would mean that I want to quit the game so I need to skip over everythingelse
            return
        self.screen.fill(bg) #fills screen white
        self.draw_text("GAME OVER", 96, black, width / 2, height / 4) #draws the text
        #self.draw_text("Score: " + str(self.score), 48, black, width / 2, height / 2.5)
        self.draw_text("Press any key to play again", 30, black, width / 2, height * 3 / 4)
        pygame.display.flip() #flips display
        self.wait_for_key() #waits for key to be pressed until you play another game

    def message_display(self,text):
        self.stime = time.localtime(time.time())[5]
        self.largeText = pygame.font.Font('freesansbold.ttf', 115)
        self.textsurf, self.textrect = self.text_objects(text, self.largeText)
        self.textrect.center = ((width / 2), (height / 2))
        self.screen.blit(self.textsurf, self.textrect)
        pygame.display.update()


    def crash(self):
        self.message_display('You Crashed')
        self.playing = False

    def wait_for_key(self): #function for when you are waiting for a key
        waiting = True
        while waiting:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #this is so that if you click the x then you will be able to quit
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:#here once you hit any key then you no longer need to wait
                    waiting = False


class Coin(pygame.sprite.Sprite):
    def __init__ (self,screen, x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('coin.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        screen.blit(self.image, (x, y))

class Stripe(pygame.sprite.Sprite):
    def __init__ (self,screen, y):
        pygame.sprite.Sprite.__init__(self)
        self.y = y
        self.screen = screen
        pygame.draw.rect(self.screen, black, [240, self.y, 20, 50])



g = Game()
#g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pygame.quit()
