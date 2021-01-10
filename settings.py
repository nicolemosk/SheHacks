title = "My Game"

width = 480
height = 600
fps = 60

font_name = 'Helvetica'

#player properties
player_acc = 0.5
player_friction = -0.1
player_grav = 0.8
player_jump = 20

#game properties
player_layer = 2
platform_layer = 1
coin_layer = 1
mob_layer = 2
cloud_layer = 0

#starting platforms
platform_list = [(0, height-60),
                 (width/2 - 50, height *3/4 - 50 ),
                 (125, height -350),
                 (350, 200 ),
                 (175, 100)]


#x,y, width, thickness

#difining colours
white = (255,255,255)
black = (0,0,0)
red = (255, 0, 0)
green = (0,255,0)
blue = (0,0,255)
yellow = (255,255,0)
lightblue=(180,255,255)
bgcolour= lightblue