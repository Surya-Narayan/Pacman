import pygame
vec=pygame.math.Vector2()
from settings import *
class Player:
    def __init__(self,app,pos):
        self.app=app
        self.grid_pos=pos
        self.pix_pos=self.get_pix_pos()
        self.direction=vec(1,0)
        print(self.pix_pos,self.grid_pos)

    def get_pix_pos(self):
        return vec(self.grid_pos.x*self.app.cell_width + TOP_BOTTOM_BUFFER//2 + self.app.cell_width//2 
        ,self.grid_pos.y*self.app.cell_height + TOP_BOTTOM_BUFFER//2 + self.app.cell_width//2 )
          

    def update(self):
        self.pix_pos+=self.direction
        # Setting grid pos wrt pixel pos
        self.grid_pos[0]=(self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width//2 )//self.app.cell_width +1
        self.grid_pos[1]=(self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height//2 )//self.app.cell_height +1

    def draw(self):
        # pygame.draw.rect(self.app.screen,RED,(self.grid_pos[0]*self.app.cell_width+ TOP_BOTTOM_BUFFER//2,self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2,self.app.cell_width,self.app.cell_height))
        pygame.draw.rect(self.app.screen, RED, (self.grid_pos[0]*self.app.cell_width+TOP_BOTTOM_BUFFER//2,
                                                self.grid_pos[1]*self.app.cell_height+TOP_BOTTOM_BUFFER//2, self.app.cell_width, self.app.cell_height), 1)

        pygame.draw.circle(self.app.screen,PLAYER_COLOUR,(int(self.pix_pos.x),int(self.pix_pos.y)),self.app.cell_width//2-2 )

    def move(self,direction):
        self.direction=direction