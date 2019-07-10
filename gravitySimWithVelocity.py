import beam
import random
from random import *
import math
from math import *
import pygame
from pygame import *
import time
from time import *
import sys
import os
import sys
import Quadmove
import trig


cpos = (1000,1050)
scale = 16
dist = 100
num = 100
dline = False
size = 13
ran = 2
speed = 1

WIDTH = 1200
HEIGHT = 700
GS = 6.67*(10**-11)
collisions = []

def gravCalc(mass,distance):                   #uses the equation Gm1m2/r2 or Gm1/r2 to calculate gravitational feild strength
  g = (GS*mass/(distance)**2)
  return g

class particle:                                 #objects that the program uses
  def __init__(self,name,mass,x,y):
    self.mass = mass
    self.name = name
    self.density = 10**10
    self.x = x
    self.y = y
    self.velocityx = 0
    self.velocityy = 0

  def draw(self):          # draws the object on, proportional to mass and density to calculate volume and then radius
    volume = self.mass/self.density
    rrad = int(sqrt(volume/3.14))
    rad = int(rrad / scale)
    try:               # some objects are too large to draw :(
      pygame.draw.circle(DISPLAY,(255,255,255),(int((WIDTH/2)+(int(self.x/scale)-(cpos[0]/scale))),int((HEIGHT/2)+(int(self.y/scale)-(cpos[1]/scale)))),rad)
    except:
      pass

  def move(self,t):                                           # moves the object
    self.x = (self.velocityx*t + self.x)#%(WIDTH*scale)
    self.y = (self.velocityy*t+self.y)#%(HEIGHT*scale)
  
  def smove(self,objs,line,t):                                                          # honestly need to work on naming stuff
    #gs.append(str(self.velocityx*self.mass)+str('  ,  ')+str(self.velocityy*self.mass))
    xMove = 0
    yMove = 0
    ext = False
    for obj in objs:                          # gravitation force from each object needed
      if obj !=  self:
        xchange = obj.x - self.x
        ychange = obj.y-self.y
        volume = self.mass/self.density
        rad = int(sqrt(volume/3.14))
        if beam.intercept(self.x,self.y,self.x+self.velocityx*t,self.y+self.velocityy*t,obj.y-rad,obj.x-rad,2*rad,2*rad,True):   # what to do if objects collide, otherwise stuff gets flung through by a ridiculous amount of gravity 
          global objects
          collisions.append(obj.name+' collided with '+self.name)
          smoment = (self.velocityx*self.mass,self.velocityy*self.mass)
          obmoment = (obj.velocityx*obj.mass,obj.velocityy*obj.mass)
          tmoment = (smoment[0]+obmoment[0],smoment[1]+obmoment[1])
          self.mass += obj.mass
          self.velocityx += tmoment[0]/self.mass
          self.velocityy += tmoment[1]/self.mass
          objs.remove(obj)
          objects = order(objects)
        else:                             # if the objects dont collide, how do they accelerate each other?
          dist = sqrt((xchange)**2+(ychange)**2)           # distance between objects
          g = gravCalc(obj.mass,dist)                     # calculate g between objects
          #gs.append(str(g))
          deg = trig.finddeg(xchange,ychange)               # calculate the degree between them to convert t=g into a vector
          xMove,yMove = trig.degtosides(deg,g)              # turn g into a vector
          if line:
            pygame.draw.line(DISPLAY,(10,10,10),(int(self.x/scale),int(self.y/scale)),(int(obj.x/scale),int(obj.y/scale)),int(g/scale)+1)  # draw lines to show g

    gs.append(str(sqrt(xMove**2+yMove**2)))
    self.velocityx += xMove*t                    # change velocities based on the total accelerations of the 
    self.velocityy += yMove*t
    #pygame.draw.line(DISPLAY,(160,0,0),(int(self.x/scale),int(self.y/scale)),(int((self.x+(self.velocityx*100))/scale),int((self.y+(self.velocityy*100))/scale)),3)



def addpart(s,x,y):
  objects.append(particle(str(randint(1,10000)),s,x,y))

def cvel(x,y,n):
  objects[n].velocityy +=y
  objects[n].velocityx += x

def order(lis):
  arrange = {}
  for l in lis:
    if arrange.get(l.mass) == None:
      arrange[l.mass] = [l]
    else:
      arrange[l.mass] += [l]
  newarr = []
  for i in range(len(arrange)):
    tag = arrange[min(arrange)]
    for t in tag:
      newarr.append(t)
    del arrange[min(arrange)]
  return newarr


objects = []   # array of objects

#random sim

#for i in range(num):
  #objects.append(particle(str(i),randint(10**size,10**(ran+size)),randint(1,WIDTH*dist),randint(1,HEIGHT*dist)))


# earth sun sim - earth moving at 30km/s billions of km away


#addpart(2*10**30,0,0)
#addpart(6*10**24,1.4*10**11,0)
#cvel(0,30000,1)


#mini solar system - v small

addpart(2*10**12,2000,1050)
addpart(2*10**12,1800,750)
addpart(3*10**12,2000,1500)
addpart(10**12,1800,30)
addpart(10**10,1800,200)
addpart(10**9,1500,1400)
addpart(10**12,1800,4000)
addpart(10**8,1800,1150)

addpart(10**14,1800,1050)              # little solar system i built. Highly unrealistic as all objects are only hundreds of meters away, but makes it easier to understand
 
cvel(-8,0,7)
cvel(0,6,0)
cvel(5,0,1)
cvel(-4,0,2)
cvel(2.5,0,3)
cvel(2,0,4)
cvel(-2,-2,5)
cvel(-1.5,0,6)




gs = []
objects = order(objects)
pygame.init()
DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT),FULLSCREEN)

#main loop for GUI

def run():
  tim = 0
  n = time()
  c = 0
  screens = []
  cur = 1
  while True:
    global gs,objects,cpos,scale,speed
    l = time()
    t = (l-n)*speed   # calculates the amount of time passed in the previous iteration, so that this time can be used to accuratly calculate velocities (multiplied by speed to speed things up  byy a multiplier)
    tim+=t   # adds to running total time passed
    n = time()
    gs = []
    gs.append('Speed: '+str(speed)+'x')
    c+=1
    DISPLAY.fill((0,0,0))
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE: # if escape 
          print(tim/31536000)        # prints total time elapsed
          pygame.quit()             #quits
          sys.exit()
        if event.key == K_RIGHT:   # right and left key to move through  which object to focus on
          cur += 1
          cur = cur%len(objects)
        if event.key == K_LEFT:
          cur -= 1
          cur = cur%len(objects)
        if event.key == K_UP:     # up and down scale rapidly (change the size of what can be seen)
          scale = scale * 2
        if event.key == K_DOWN:
          scale = scale / 2
        if event.key == K_3:       # 3 and 4 move the scale more slowly
          scale += 1
        if event.key == K_4 and scale > 2:
          scale-= 1
        if event.key == K_2:                 # 1 and 2 increase and decrease speed (actuall speed is deafult)
          speed = speed * 2
        if event.key == K_1 and speed > 1:
          speed = speed / 2
    for obj in objects:
      obj.smove(objects,dline,t)    # calculates gravity affecting the object. as F = mg and F = mg, we have calculated g and g = a, so we know the acceleration. we can multiply this by time taken to change velocity
    for obj in objects:
      obj.move(t)                    # acctually changes the coordinates of the objects
    cpos = (objects[-cur].x,objects[-cur].y)   # sets the camera position
    for obj in objects:
      obj.draw()                     # draws on all the objects
    d = 10
    myfont = pygame.font.SysFont('Comic Sans MS', 10)
    #for collision in collisions[-60:]:
    #  textsurface = myfont.render(collision, False, (0, 255, 0))
    #  DISPLAY.blit(textsurface,(5,d))
    #  d+=10
    for g in gs:
      textsurface = myfont.render(g, False, (0, 255, 0))                # text information. think is displaying GFS
      DISPLAY.blit(textsurface,(5,d))
      d+=10
    if c%2 == 0:
      pygame.draw.rect(DISPLAY,(255,0,0),(WIDTH-10,HEIGHT-10,10,10)) # weird cube to show how often frame changes. Not relevant due to time added
    if c % 200 == 0:                       # weird bit of code to save frames every 200. don't know why, havent used
      screens.append(DISPLAY)   
    pygame.display.update()     # GUI stuff

run()
