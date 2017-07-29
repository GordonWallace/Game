#Imports
import pygame, os, math, numpy
from pygame.locals import *
from pygame.compat import geterror

clock = pygame.time.Clock() #Used to set ticks
pctgrass = numpy.random.randint(20,80)/100
        
#Image loading function
def loadimage(imgfile,x,y):
    data_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'data')
    img = pygame.image.load(os.path.join(data_dir,imgfile))
    img = img.convert()
    return img, img.get_rect(topleft = (x,y))

#Block parent class
class block(pygame.sprite.Sprite):
    def __init__(self):
        pass
    def dig(self):
        if not isinstance(self, bedrock):
            self.kill()
    
#Dirt class
class dirt(block):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.grass = numpy.random.choice([True,False], p = [pctgrass, 1-pctgrass])
        if self.grass:
            imgfile = 'grass.jpg'
        else:
            imgfile = 'dirt.jpg'
        self.image, self.rect = loadimage(imgfile,x,y)

#Bedrock class
class bedrock(block):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadimage('bedrock.png',x,y)

#Sand class
class sand(block):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadimage('sand.jpg',x,y)

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
        x,y = pygame.mouse.get_pos()
        self.image, self.rect = loadimage('fist.bmp',x,y)
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
    top = [None]*xdim*ydim
    topmap = [[None]*xdim]*ydim
    count = 0
    x = 0
    y = 0
    for i in range(ydim):
        for j in range(xdim):
            bdrk[count] = bedrock(x,y)
            
            top[count] = sand(x,y)
            count += 1
            x += res
        y += res
        x -= res*xdim
    blockgrp = pygame.sprite.RenderPlain(bdrk,top)
    fstgrp = pygame.sprite.RenderPlain(fist)
    blockgrp.draw(screen)
    fstgrp.draw(screen)
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
                blockhitlist = pygame.sprite.spritecollide(fist, blockgrp, False)
                for k in blockhitlist:
                    k.dig()
        blockgrp.update()
        fstgrp.update()
        screen.blit(background, (0, 0))
        blockgrp.draw(screen)
        fstgrp.draw(screen)
        pygame.display.flip()
    pygame.quit()

#Calls main function    
if __name__ == '__main__':
    main()
