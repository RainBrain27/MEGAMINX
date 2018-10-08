import Shared as s
import Einheitskreis as E
from math import *

class Koordinate():
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z

class Point(Koordinate):
    def __init__(self,x,y,z):
        s.P_list.append(self)
        #self.count=0
        Koordinate.__init__(self,x,y,z) # absolute koordinaten im koordinatensysthem

    def turn(self,DP_x,DP_y,DP_z,w_x,w_y,w_z):
        self.x,self.y,self.z = E.turn_p(self.x,self.y,self.z,DP_x,DP_y,DP_z,w_x,w_y,w_z)

    def move(self,a,b,c):
        self.x+=a
        self.y+=b
        self.z+=c
    
if __name__=="__main__":
    import MAIN


