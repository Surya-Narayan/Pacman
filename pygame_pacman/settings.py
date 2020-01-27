from pygame.math import Vector2 as vec
#Screen Settings
WIDTH , HEIGHT = 610,670
TOP_BOTTOM_BUFFER=50
MAZE_WIDTH , MAZE_HEIGHT = WIDTH-TOP_BOTTOM_BUFFER,HEIGHT-TOP_BOTTOM_BUFFER
FPS=60


#color settings
BLACK=(0,0,0)
RED=(200,20,20)
GREY=(107,107,107)
WHITE=(25,255,255)
PLAYER_COLOUR=(190,194,15)
#font settings
START_TEXT_SIZE=16
START_FONT='arial black'


#player settings
PLAYER_START_POS= vec(1,1)
#mob settings