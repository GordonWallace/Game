#V2
#Imports
import pygame
import os
import math
import numpy
from pygame.locals import *
from pygame.compat import geterror

clock = pygame.time.Clock() #Used to set ticks
pctgrass = numpy.random.randint(20,80)/100
print(pctgrass)
        
#Convenient stuff for importing images and sounds
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

#Block parent class
class block(pygame.sprite.Sprite):
    def __init__(self):
        pass
    
#Bedrock class
class dirt(block):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.grass = numpy.random.choice([True,False], p = [pctgrass, 1-pctgrass])
        if self.grass:
            self.image = pygame.image.load(os.path.join(data_dir,'grass.jpg'))
        else:
            self.image = pygame.image.load(os.path.join(data_dir,'dirt.jpg'))
        self.rect = self.image.get_rect(topleft = (x,y))
    def dig(self):
        self.kill()

#Dirt class
class bedrock(block):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(data_dir,'bedrock.png'))
        self.rect = self.image.get_rect(topleft = (x,y))
        
#Inventory class
class inventory(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(data_dir,'blank.jpg'))
        self.rect = self.image.get_rect()
        self.dirt = 0
        self.stone = 0
    def additem(self):
        pass

#Fist class
class Fist(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(data_dir,'fist.bmp'))
        self.rect = self.image.get_rect()
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        
#Main function
def main():
    #Initializes pygame
    pygame.init()
    screenx = 600
    screeny = 900
    screen = pygame.display.set_mode((screenx, screeny))
    pygame.display.set_caption('Hello')
    pygame.mouse.set_visible(0)
    
    #Creates, displays the backgound
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((100, 100, 255))
    screen.blit(background, (0,0))

    #Creates objects
    fist = Fist()
    res = 90
    xdim = math.ceil(screenx/res)
    ydim = math.ceil(screeny/res)
    bdrk = [None]*xdim*ydim
    drt = [None]*xdim*ydim
    count = 0
    x = 0
    y = 0
    for i in range(ydim):
        for j in range(xdim):
            bdrk[count] = bedrock(x,y)
            drt[count] = dirt(x,y)
            count += 1
            x += res
        y += res
        x -= res*xdim
    allsprites = pygame.sprite.RenderPlain((bdrk,drt,fist))
    allsprites.draw(screen)
    pygame.display.flip()
    
    #Main loop
    going = True
    while going:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                going = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False
            elif event.type == MOUSEBUTTONDOWN:
                blockhitlist = pygame.sprite.spritecollide(fist, allsprites, False)
                for k in range(len(blockhitlist)):
                    if isinstance(blockhitlist[k], dirt):
                        blockhitlist[k].dig()
        allsprites.update()
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pygame.display.flip()
    pygame.quit()

#Calls main function    
if __name__ == '__main__':
    main()
