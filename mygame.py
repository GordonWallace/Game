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

#Mapmaker function
def whattype(locx,locy,topmap,types):
    dirtc = 0.01
    sandc = 0.01
    if locx == 0:
        lowx = 0
    else:
        lowx = locx-1
    if locy == 0:
        lowy = 0
    else:
        lowy = locy-1
    if locx == len(topmap)-1:
        highx = locx+1
    else:
        highx = locx+2
    if locy == len(topmap[0])-1:
        highy = locy+1
    else:
        highy = locy+2
    for i in range(lowx,highx):
        for j in range(lowy,highy):
            if topmap[i][j] == 'dirt':
                dirtc += 1
            elif topmap[i][j] == 'sand':
                sandc += 1
    dirtp = dirtc/(dirtc+sandc)
    if dirtp > 0.99:
        dirtp = 0.99
    if dirtp < 0.01:
        dirtp = 0.01
    return numpy.random.choice(types, p=[dirtp,1-dirtp])

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
            imgfile = 'grass.jpg'
        self.image, self.rect = loadimage(imgfile,x,y)

#Bedrock class
class bedrock(block):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadimage('bedrock.png',x,y)

#Stone class
class stone(block):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = loadimage('stone.png',x,y)

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
        self.image, self.rect = loadimage('pointer.png',x,y)
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.midtop = pos
        
#Main function
def main():
    #Initializes pygame
    pygame.init()
    screenx = 2560
    screeny = 1440
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
    bdrk = [[ None for i in range(xdim)] for j in range(ydim)]
    stn = [[ None for i in range(xdim)] for j in range(ydim)]
    top = [[ None for i in range(xdim)] for j in range(ydim)]
    topmap = [[ None for i in range(xdim)] for j in range(ydim)]
    types = ['dirt','sand']
    #xmap,ymap = math.ceil(xdim/2), math.ceil(ydim/2)
    xmap = 0
    ymap = 0
    topmap[xmap][ymap] = numpy.random.choice(types)
    count = 0
    x = 0
    y = 0
    for i in range(ydim):
        for j in range(xdim):
            bdrk[i][j] = bedrock(x,y)
            stn[i][j] = stone(x,y)
            topmap[i][j] = whattype(i,j,topmap,types)
            if topmap[i][j] == 'dirt':
                top[i][j] = dirt(x,y)
            elif topmap[i][j] == 'sand':
                top[i][j] = sand(x,y)
            x += res
        y += res
        x -= res*xdim
    lvl1 = pygame.sprite.RenderPlain(bdrk)
    lvl2 = pygame.sprite.RenderPlain(stn)
    lvl3 = pygame.sprite.RenderPlain(top)
    fstgrp = pygame.sprite.RenderPlain(fist)
    lvl1.draw(screen)
    lvl2.draw(screen)
    lvl3.draw(screen)
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
                blockhitlist = pygame.sprite.spritecollide(fist, lvl3, False)
                for k in blockhitlist:
                    k.dig()
        lvl1.update()
        lvl2.update()
        lvl3.update()
        fstgrp.update()
        screen.blit(background, (0, 0))
        lvl1.draw(screen)
        lvl2.draw(screen)
        lvl3.draw(screen)
        fstgrp.draw(screen)
        pygame.display.flip()
    pygame.quit()

#Calls main function    
if __name__ == '__main__':
    main()
