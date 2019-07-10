import random
from random import *
import math
from math import *
import pygame
from pygame import *
import sys
import os
import sys
import Quadmove
import trig

WIDTH = 1200
HEIGHT = 700


def intercept(sx,sy,ex,ey,TOP,LEFT,WIDTH,HEIGHT,step):
  cx = ex-sx
  cy = ey-sy
  if cy == 0:
    if TOP<=sy<=TOP+HEIGHT:
      if step:
        LEFT -= sx
        if cx < 0 and LEFT < 0:
          LEFT = -LEFT-WIDTH
          cx = -cx
        if 0<= LEFT <= cx:
          return True
        else:
          return False
      else:
        return True
    else:
      return False
  elif cx == 0:
    if LEFT<=sx<=LEFT+WIDTH:
      if step:
        TOP -= sy
        if cy < 0 and TOP < 0:
          TOP = -TOP-HEIGHT
          cy = -cy
        if 0<= TOP <= cy:
          return True
        else:
          return False
      else:
        return True
    else:
      return False
  else:
    LEFT -= sx
    TOP -= sy
    gradient = cy/cx
    if LEFT<=TOP/gradient<=LEFT+WIDTH or LEFT<=(TOP+HEIGHT)/gradient<=LEFT+WIDTH or TOP<=LEFT*gradient<=TOP+HEIGHT or TOP<=(LEFT+WIDTH)*gradient<=TOP+HEIGHT:
      if step:
        if cx < 0 and LEFT < 0:
          LEFT = -LEFT-WIDTH
          cx = -cx
        if cy < 0 and TOP < 0:
          TOP = -TOP-HEIGHT
          cy = -cy
        if (0<= LEFT <= cx or LEFT <= cx <= LEFT+WIDTH) and (0<= TOP <= cy or TOP <= cy<= TOP+HEIGHT):
          return True
        else:
          return False
      else:
        return True
    else:
      return False


class box:
  def __init__(self,x,y,height,width):
    self.x = x
    self.y = y
    self.h = height
    self.w = width

  def draw(self):
    pygame.draw.rect(DISPLAY,(255,255,255),(self.x,self.y,self.w,self.h))

  def test(self,beam):
    if intercept(beam.x,beam.y,beam.ex,beam.ey,self.y,self.x,self.w,self.h,True):
      boxes.remove(self)
    else:
      self.draw()

class beam:
  def __init__(self,x,y):
    self.x = x
    self.y = y
    self.ex = x
    self.ey = y
    self.prev = (0,1)

  def update(self,mx,my):
    self.ex = mx
    self.ey = my
    self.draw()

  def draw(self):
    cx,cy = self.ex-self.x,self.ey-self.y
    if cx ==0 and cy == 0:
      cx,cy = self.prev
    else:
      self.prev = (cx,cy)
    pygame.draw.line(DISPLAY,(255,0,0),(self.x,self.y),(self.ex,self.ey),2)


def spawn():
  boxes.append(box(randint(1,WIDTH-10),randint(1,HEIGHT-10),randint(6,30),randint(6,30)))

boxes = []
boxes.append(box(570,340,20,5))


def run():
  pygame.init()
  global DISPLAY,you
  DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT),FULLSCREEN)
  you = beam(600,350)
  c = 0
  while True:
    c+=1
    DISPLAY.fill((0,0,0))
    for event in pygame.event.get():
      if event.type == KEYDOWN:
        if event.key == K_ESCAPE:
          pygame.quit()
          sys.exit()
    mx,my = pygame.mouse.get_pos()
    you.update(mx,my)
    for b in boxes:
      b.test(you)

    pygame.display.update()
    spawn()
  
  
#run()

