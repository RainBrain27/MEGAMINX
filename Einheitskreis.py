import Shared as s
import math as m

"""
turn_s:
    berechnet verhaltnis/lange
    von ankatete zu gegenkatete bei
    winkelveränderung
r1:
    berechnet strecken zwischn zwei punkten
r2:
    brechnet aus drehpunkt und strecken den punkt
turn:
    koordiniert dei veranderungen der streckenlangen
    durch drehungen um die einzelnen achsen
"""

def turn_s(ak,gk,add):
    if not ak==gk==0:
        hy = m.sqrt(ak**2+gk**2)
        #===Berechnung Sektor/Winkel===#
        w = m.asin(gk/hy)
        if ak <0:
            w=m.pi-w
        #===addieren vom Winkel===#
        w+=add*s.grad
        #===Berechnumg der Seiten===#
        gk = m.sin(w)*hy
        ak = m.cos(w)*hy
    return ak,gk



#verbundsfunktion
def turn_p(x,y,z,DP_x,DP_y,DP_z,wx,wy,wz):
    a,b,c = r1(x,y,z,DP_x,DP_y,DP_z)
    a,b,c = turn(a,b,c,wx,wy,wz)
    x,y,z = r2(a,b,c,DP_x,DP_y,DP_z)
    return x,y,z


#berechnet strecken zwischn zwei punkten
def r1(x,y,z,DP_x,DP_y,DP_z):
    a = x - DP_x
    b = y - DP_y
    c = z - DP_z
    return a,b,c


#brechnet aus drehpunkt und strecken den punkt
def r2(a,b,c,DP_x,DP_y,DP_z):
    x = DP_x+a
    y = DP_y+b
    z = DP_z+c
    
    return x,y,z

#drehung der strecken um alle winkel
def turn(a,b,c,wx,wy,wz):
    if wy!=0:             #vermeidung division by zero
        a,c = turn_s(a,c,wy)
    if wx!=0:
        c,b = turn_s(c,b,wx)
    if wz!=0:
        a,b = turn_s(a,b,wz)

    return a,b,c

def turn2(a,b,c,wx,wy,wz):
    if wz!=0:
        a,b = turn_s(a,b,wz) # Reihenfolge negiert
    if wx!=0:
        c,b = turn_s(c,b,wx)     # Reihenfolge negiert
    if wy!=0:             #vermeidung division by zero
        a,c = turn_s(a,c,wy)
    
    

    return a,b,c


if __name__=="__main__":
    import MAIN

