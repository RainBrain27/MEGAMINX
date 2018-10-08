import Shared as s

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

import Punkt as P
#import Bind
#import Special_Objekts as O
import Megaminx as meg

import random
    
#============================================

def create():
    a=1
    x=0
    y=0
    z=0
    s.MEGAMINX=meg.Megaminx(x,y,z)
    '''
    0,0,0     black
    255,0,0   red
    0,255,0   green
    0,0,255   blue
    0,255,255 türkis
    255,0,255 rosa
    255,255,0 yellow
    255,255,255 white
    
    '''
def window():
    pygame.init()
    display = (1000,800)
    #display = (1920,1080)
    pygame.display.set_caption("MEGAMINX")
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

    glEnable (GL_DEPTH_TEST)

    gluPerspective(45, (display[0]/display[1]), 0.5, 10000.0)
    #(sichtbare gradzahl(legt FP_z fest),?,clippingebene vorne,hinten)

    glTranslatef(0,0, -20)

    #glRotatef(25, 2, 1, 0)
    #rotating perspective

def main():
    W=0
    A=0
    S=0
    D=0
    rotate=0

    init()
    
    while True:
        f=1
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    W=1
                if event.key == pygame.K_a:
                    A=1

                if event.key == pygame.K_s:
                    S=1
                if event.key == pygame.K_d:
                    D=1


                if event.key == pygame.K_LSHIFT:
                    s.button[12]=1

                for i in range(12):
                    if eval("event.key == pygame.K_"+s.BUTTON[i]):
                        if s.button[i]==0:
                            s.MEGAMINX.mod=3
                            s.MEGAMINX.desolve()
                            s.MEGAMINX.exec_add(i, s.button[12]*2-1)
                        s.button[i]=1

                if event.key == pygame.K_m:
                    s.MEGAMINX.mix(100)

                if event.key == pygame.K_n:
                    s.MEGAMINX.solve()

                if event.key == pygame.K_b:
                    s.MEGAMINX.set_skip=1

                if event.key == pygame.K_v:
                    s.MEGAMINX.back()
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    W=0
                if event.key == pygame.K_a:
                    A=0
                if event.key == pygame.K_s:
                    S=0
                if event.key == pygame.K_d:
                    D=0

                if event.key == pygame.K_LSHIFT:
                    s.button[12]=0
                for i in range(12):
                    if eval("event.key == pygame.K_"+s.BUTTON[i]):
                        s.button[i]=0

                if event.key == pygame.K_b:
                    s.MEGAMINX.set_skip=0

            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if event.button == 4:
                    glTranslatef(0,-0.5*f,0)

                if event.button == 5:
                    glTranslatef(0,0.5*f,0)

                if event.button == 1:
                    rotate=1
                    #relative koord. reseten
                    pygame.mouse.get_rel()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    rotate=0

        #===============
        if (W):
            glTranslatef(0,0,0.2*f)
        if (S):
            glTranslatef(0,0,-0.2*f)
        if (A):
            glTranslatef(0.1*f,0,0)
        if (D):
            glTranslatef(-0.1*f,0,0)
        if (rotate):#RICHTIG? NEIN !
            #Drehen der Camera
            rel=pygame.mouse.get_rel()
            #relative mauskoordinaten werden ermittelt
            s.pitch+=rel[1]/5
            s.yaw+=rel[0]/5
            
        #===============
        glRotatef(s.pitch, 1, 0, 0)
        glRotatef(s.yaw, 0, 1, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        draw()
        pygame.display.flip()
        glRotatef(-s.yaw, 0, 1, 0)
        glRotatef(-s.pitch, 1, 0, 0)
        pygame.time.wait(10)
        action()

def init():
    #s.MEGAMINX.mix(1000)
    global solve_f
    solve_f = 1
    
def action():
    global solve_f
    #if solve_f == 1:
    #    if s.MEGAMINX.mod==0:
    #        s.MEGAMINX.solve()
    #        solve_f = 0
    #print (s.MEGAMINX.exec_list)
    s.MEGAMINX.tick()
    
    pass

def draw():
    '''
    for polygon in s.polygon_list:
        glBegin(GL_POLYGON)
        glColor3fv(polygon.color)
        for p in polygon.P_list:
            glVertex3f(p.x,p.y,p.z)
            #print(p.x,p.y,p.z)
        glEnd()
        glBegin(GL_LINE_LOOP)
        glColor3fv((0,0,0))
        for p in polygon.P_list:
            glVertex3fv((p.x,p.y,p.z))
        glEnd()
    '''
    #rand=random.randint(0,10)
    for i in range (12):
        for j in range(11):
            glBegin(GL_POLYGON)
            glColor3fv(s.MEGAMINX.color[s.MEGAMINX.seiten[i][j][0]])
            #glColor3fv(s.MEGAMINX.color[s.MEGAMINX.seiten[i][rand][0]])
            for p in s.MEGAMINX.polygons[i][j]:
                glVertex3f(
                    p.x,#+(random.random()/25),
                    p.y,#+(random.random()/25),
                    p.z,#+(random.random()/25)
                    )
            glEnd()
            
            #'''
            glBegin(GL_LINE_LOOP)
            glColor3fv((0,0,0))
            for p in s.MEGAMINX.polygons[i][j]:
                glVertex3f(p.x,p.y,p.z)
            glEnd()
            #'''
            
    for pol in s.MEGAMINX.black:
        glBegin(GL_POLYGON)
        glColor3fv((0,0,0))
        for p in pol:
            glVertex3f(p.x,p.y,p.z)
        glEnd()

#============================================
        
def start():
    create()
    window()
    main()
#============================================

start()

