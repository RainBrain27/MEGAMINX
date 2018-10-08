import Punkt as P
import math as m
import Shared as s
import random
    

class Megaminx():
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        self.FFW=m.acos(-m.sqrt(5)/5)/s.grad
        
        self.r=self.radius()
        self.polygons = self.create()
        self.colors()
        self.strukture()
        self.muster()
        #DP        = self.drehpunkt()

        #BO.Objekt.__init__(self,P_list,polygon_list,DP)

        self.roll=0
        self.rollv=[0,0,0]#seite,richtung,winkel
        self.black=[]

        self.mod=0
        '''
        self.mod
        0=NOTHING
        1=MIXING
        2=SOLVING
        '''
        self.exec_f=0
        self.exec_list=[]

        self.solve_mod=0
        self.solve_count=0
        self.moves=0

        self.skip=0
        self.set_skip=0

        self.reset_f=0

        self.reset=[]

    def exec_add(self,i,n):
        self.exec_list.append((i,n))
        if self.exec_f==0:
            self.exec_f=1
        self.moves+=1

    def desolve(self):
        self.solve_mod=0
        self.mod=0
        self.exec_list=[]
        self.moves=0

    def mix(self,n):
        self.desolve()
        if (self.mod==0):
            self.mod =1
            
            for i in range(n):
                self.exec_list.append((random.randint(0,11),1))#random.randint(0,1)*2-1))
                self.exec_f=1

            self.set_skip=0
                
    def solve(self):
        self.desolve()
        if self.mod==0:
            self.mod=2

            self.set_skip=0
            #
            #self.solve_count=0
            self.solve_mod=1

    def solve_1(self):
        t=5
        for i in range(5):
            if self.parts[0][i*2+1]!=self.muster[0][i*2+1]:
                if t==5:
                    t=i
        if t!=5:
            for i in range(12):
                for j in range(5):
                    if self.muster[0][t*2+1]==self.parts[i][j*2+1]:
                        if i == 11: #fall 1
                            #print ("1")
                            for r in range(5):
                                if self.nei[11][r]==self.nei[ self.nei[0][t] ][4]:
                                    self.move_ft(11,j,r)                                            
                            self.exec_add(self.nei[ self.nei[0][t] ][4],1)
                            self.exec_add(self.nei[ self.nei[0][t] ][0],-1)
                            self.exec_add(self.nei[0][t],1)
                            self.exec_add(self.nei[0][t],1)
                            
                        elif 11>i>5: #fall 2 #überführung in fall 1
                            #print("2")
                            self.move_ft(i,j,3)
                            self.exec_add(self.nei[i][3],1)
                        elif 6>i>0: #fall 3
                            #print ("3")
                            
                            self.move_ft(i,j,1)
                            for r in range(5):
                                if self.nei[0][r]==self.nei[i][1]:
                                    self.move_ft(0,t,r)      
                                    self.exec_add(self.nei[i][1],-1)
                                    self.move_ft(0,r,t)

                            if self.nei[0][t]!=i:
                                self.move_ft(i,1,j)
                            #'''

                        elif i==0: # fall 4 # überführung in fall 3
                            #print ("4")
                            self.exec_add(self.nei[i][j],1)
        else:
            self.solve_mod+=1

    def solve_2(self):
        t=5
        for i in range(5):
            if self.parts[0][i*2]!=self.muster[0][i*2]:
                if t==5:
                    t=i
        if t!=5:
            for i in range(12):
                for j in range(5):
                    if self.muster[0][t*2]==self.parts[i][j*2]:
                        if i == 11: #fall 1 #--> fall 2
                            #print ("2.1")
                            self.exec_add(self.nei[11][j],1)
                            
                        elif 11>i>5: #fall 2 #main
                            #print("2.2")
                            self.move_ft(i,j,2)
                            
                            for B in range(5):
                                if self.nei[11][B]==self.nei[self.nei[0][t]][0]:
                                    b=B
                            for A in range(5):
                                if self.nei[11][A]==i:
                                    a=A
                            self.move_ft(11,a,b)
                            
                            self.exec_add(self.nei[self.nei[0][t]][4],-1)
                            self.exec_add(self.nei[self.nei[0][t]][4],-1)
                            self.exec_add(self.nei[0][t],1)
                            self.exec_add(self.nei[self.nei[0][t]][4],-1)
                            self.exec_add(self.nei[0][t],-1)
                            
                        elif 6>i>0: #fall 3 #-->fall 2
                            #print ("2.3")
                            if j in (1,2):
                                self.exec_add(i,-1)
                                self.exec_add(self.nei[i][0],1)
                                self.exec_add(i,1)
                            elif j in(3,4):
                                self.exec_add(i,1)
                                self.exec_add(self.nei[i][4],-1)
                                self.exec_add(i,-1)
                            else:
                                self.exec_add(self.nei[i][0],1)   

                        elif i==0: # fall 4 # überführung in fall 2
                            #print ("2.4")

                            
                            self.exec_add(self.nei[0][j],1)
                            self.exec_add(self.nei[self.nei[0][j]][4],1)
                            self.exec_add(self.nei[0][j],-1)

                            
        else:
            self.solve_mod+=1

    def solve_3(self):
        t=5
        for i in range(5):
            if self.parts[self.nei[0][i]][3*2+1]!=self.muster[self.nei[0][i]][3*2+1]:
                if t==5:
                    t=i
        if t!=5:
            for i in range(12):
                for j in range(5):
                    if self.muster[self.nei[0][t]][3*2+1]==self.parts[i][j*2+1]:
                        if i == 11: #fall 1 #main
                            #print ("3.1")

                            for B in range(5):
                                if self.nei[11][B]==self.nei[self.nei[0][t]][4]:
                                    b=B
                            self.move_ft(11,j,b)
          
                            self.exec_add(self.nei[self.nei[0][t]][4],-1)
                            self.exec_add(self.nei[self.nei[0][t]][4],-1)
                            
                            self.exec_add(self.nei[0][t],-1)
                            self.exec_add(self.nei[0][t],-1)
                            self.exec_add(self.nei[self.nei[0][t]][0],-1)
                            self.exec_add(self.nei[self.nei[0][t]][0],-1)
                            self.exec_add(self.nei[0][t],-1)
                            self.exec_add(self.nei[0][t],-1)

                            self.exec_add(self.nei[self.nei[0][t]][4],-1)

                            self.exec_add(self.nei[0][t],1)
                            self.exec_add(self.nei[0][t],1)
                            self.exec_add(self.nei[self.nei[0][t]][0],1)
                            self.exec_add(self.nei[self.nei[0][t]][0],1)
                            self.exec_add(self.nei[0][t],1)
                            self.exec_add(self.nei[0][t],1)
                            
                        elif 11>i>5: #fall 2 #--> fall 1
                            #print("3.2")
                            self.move_ft(i,j,3)
                            self.exec_add(self.nei[i][3],1)
                            
                        elif 6>i>0: #fall 3 #--> fall 2
                            #print ("3.3")
                            if j == 1:
                                #print("0")
                                self.exec_add(i,-1)
                                self.exec_add(i,-1)
                                self.exec_add(self.nei[i][0],-1)
                                self.exec_add(self.nei[i][0],-1)

                                self.exec_add(self.nei[i][4],-1)
                                self.exec_add(self.nei[i][4],-1)

                                self.exec_add(self.nei[i][0],1)
                                self.exec_add(self.nei[i][0],1)
                                self.exec_add(i,1)
                                self.exec_add(i,1)
                                
                            elif j == 3:
                                #print("1")
                                self.exec_add(i,1)
                                self.exec_add(i,1)
                                self.exec_add(self.nei[i][4],1)
                                self.exec_add(self.nei[i][4],1)

                                self.exec_add(self.nei[i][0],1)
                                self.exec_add(self.nei[i][0],1)

                                self.exec_add(self.nei[i][4],-1)
                                self.exec_add(self.nei[i][4],-1)
                                self.exec_add(i,-1)
                                self.exec_add(i,-1)
                                
                            elif j == 4:
                                #print("2")
                                self.exec_add(self.nei[i][4],-1)
                                self.exec_add(self.nei[i][4],-1)

                            else:
                                #print("3")
                                self.exec_add(self.nei[i][0],1)
                                self.exec_add(self.nei[i][0],1)

                            
        else:
            self.solve_mod+=1
            #self.solve_4()

    def solve_4(self):
        t=5
        for i in range(5):
            if self.parts[self.nei[0][i]][4*2]!=self.muster[self.nei[0][i]][4*2]:
                if t==5:
                    t=i
        if t!=5:
            for i in range(12):
                for j in range(5):
                    if self.muster[self.nei[0][t]][4*2]==self.parts[i][j*2]:
                        if i == 11: #fall 1 #main
                            #print ("4.1")
                            for B in range(5):
                                if self.nei[11][B]==self.nei[self.nei[0][t]][4]:
                                    b=B
                            self.move_ft(11,j,b)

                            self.exec_add(self.nei[self.nei[0][t]][4],1)
                            self.exec_add(self.nei[self.nei[0][t]][4],1)
                            
                            
                        elif 11>i>5: #fall 2 #--> fall 1
                            #print("4.2")
                            if j in(0,1,2):
                                if j==0:
                                    self.exec_add(i,1)
                                self.exec_add(self.nei[i][1],-1)
                                self.exec_add(11,-1)
                                self.exec_add(11,-1)
                                self.exec_add(self.nei[i][1],1)
                            else:
                                self.exec_add(self.nei[i][3],1)
                                self.exec_add(11,1)
                                self.exec_add(11,1)
                                self.exec_add(self.nei[i][3],-1)
                            
                            
                        elif 6>i>0: #fall 3 #--> fall 2
                            #print ("4.3")
                            if j in (0,1):
                                self.exec_add(self.nei[i][0],1)
                                self.exec_add(self.nei[i][0],1)
                            else:
                                self.exec_add(self.nei[i][4],1)
                                self.exec_add(self.nei[i][4],1)

                            
        else:
            self.solve_mod+=1
            #self.set_skip=0

    def solve_5(self):
        t=5
        for i in range(5):
            for j in (1,0):
                if self.parts[self.nei[0][i]][4*j*2+1]!=self.muster[self.nei[0][i]][4*j*2+1]:
                    if t==5:
                        t=i
                        m=j
                        
        if t!=5:
            for i in range(12):
                for j in range(5):
                    if self.muster[self.nei[0][t]][4*m*2+1]==self.parts[i][j*2+1]:
                        if i == 11: #fall 1 #main
                            #print ("5.1")
                            if m==0:
                                #print ("1")
                                for B in range(5):
                                    if self.nei[11][B]==self.nei[self.nei[0][t]][4]:
                                        b=B
                                self.move_ft(11,j,b)

                                self.exec_add(self.nei[self.nei[0][t]][0],-1)
                                self.exec_add(self.nei[self.nei[0][t]][0],-1)
                                self.exec_add(11,-1)

                                self.exec_add(self.nei[self.nei[0][t]][0],1)

                                self.exec_add(11,1)
                                self.exec_add(self.nei[self.nei[0][t]][0],1)
                                self.exec_add(self.nei[self.nei[0][t]][0],1)

                            else:
                                #print ("2")
                                for B in range(5):
                                    if self.nei[11][B]==self.nei[self.nei[0][t]][0]:
                                        b=B
                                self.move_ft(11,j,b)

                                self.exec_add(self.nei[self.nei[0][t]][4],1)
                                self.exec_add(self.nei[self.nei[0][t]][4],1)
                                self.exec_add(11,1)

                                self.exec_add(self.nei[self.nei[0][t]][4],-1)

                                self.exec_add(11,-1)
                                self.exec_add(self.nei[self.nei[0][t]][4],-1)
                                self.exec_add(self.nei[self.nei[0][t]][4],-1)
                                
                            
                            
                        elif 11>i>5: #fall 2 #--> fall 1
                            #print("5.2")
                            if j in(1,2):
                                #print ("1")
                                if j == 2:
                                    self.exec_add(i,-1)
                                self.exec_add(self.nei[i][1],-1)
                                self.exec_add(11,1)
                                self.exec_add(self.nei[i][1],1)
                                if j == 2:
                                    self.exec_add(i,1)
                                
                            elif j==3:
                                #print ("2")
                                self.exec_add(self.nei[i][3],1)
                                self.exec_add(11,-1)
                                self.exec_add(self.nei[i][3],-1)

                            elif j==0:
                                #print ("3")
                                self.exec_add(i,-1)
                                self.exec_add(i,-1)
                                self.exec_add(11,-1)

                                self.exec_add(self.nei[i][3],1)
                                self.exec_add(11,1)
                                self.exec_add(self.nei[i][3],-1)

                                self.exec_add(11,1)
                                self.exec_add(i,1)
                                self.exec_add(i,1)
                            else:
                                #print ("4")
                                self.exec_add(i,1)
                                self.exec_add(i,1)
                                self.exec_add(11,1)

                                self.exec_add(self.nei[i][1],-1)
                                self.exec_add(11,-1)
                                self.exec_add(self.nei[i][1],1)

                                self.exec_add(11,-1)
                                self.exec_add(i,-1)
                                self.exec_add(i,-1)
                            
                            
                        elif 6>i>0: #fall 3 #--> fall 1
                            #print ("5.3")
                            if j==0:
                                #print ("0")
                                self.exec_add(self.nei[i][0],-1)
                                self.exec_add(self.nei[i][0],-1)
                                self.exec_add(11,-1)

                                self.exec_add(self.nei[i][0],-1)

                                self.exec_add(11,1)
                                self.exec_add(self.nei[i][0],1)
                                self.exec_add(self.nei[i][0],1)
                            else:
                                #print ("1")
                                self.exec_add(self.nei[i][4],1)
                                self.exec_add(self.nei[i][4],1)
                                self.exec_add(11,1)

                                self.exec_add(self.nei[i][4],1)

                                self.exec_add(11,-1)
                                self.exec_add(self.nei[i][4],-1)
                                self.exec_add(self.nei[i][4],-1)
                                
                                

                            
        else:
            self.solve_mod+=1
            #self.set_skip=0
            
    def solve_6(self):
        t=5
        for i in range(5):
            if self.parts[self.nei[0][i]][0]!=self.muster[self.nei[0][i]][0]:
                if t==5:
                    t=i
        
        if t!=5:
            for i in range(12):
                for j in range(5):
                    if self.muster[self.nei[0][t]][0]==self.parts[i][j*2]:
                        if i == 11: #fall 1 #--> fall 2
                            #print ("6.1")
                            for B in range(5):
                                if self.nei[11][B]==self.nei[self.nei[0][t]][4]:
                                    b=B
                            self.move_ft(11,j,b)

                            self.exec_add(self.nei[self.nei[0][t]][4],-1)
                            self.exec_add(11,-1)
                            self.exec_add(11,-1)
                            self.exec_add(self.nei[self.nei[0][t]][4],1)
                            
                            
                        elif 11>i>5: #fall 2 #main
                            #print("6.2")
                            if j == 1:
                                #print("0")
                                self.exec_add(i,1)
                                self.exec_add(11,1)
                                self.exec_add(i,-1)
                            elif j == 4:
                                #print("1")
                                self.exec_add(i,-1)
                                self.exec_add(11,1)
                                self.exec_add(i,1)

                            elif j==2:
                                #print("2")
                                for A in range(5):
                                    if self.nei[11][A]==self.nei[i][1]:
                                        a=A
                                for B in range(5):
                                    if self.nei[11][B]==self.nei[self.nei[0][t]][4]:
                                        b=B
                                self.move_ft(11,a,b)

                                self.exec_add(self.nei[self.nei[0][t]][0],1)
                                self.exec_add(11,1)
                                self.exec_add(self.nei[self.nei[0][t]][0],-1)

                            else:
                                #print("3")
                                for A in range(5):
                                    if self.nei[11][A]==i:
                                        a=A
                                for B in range(5):
                                    if self.nei[11][B]==self.nei[self.nei[0][t]][4]:
                                        b=B
                                self.move_ft(11,a,b)

                                self.exec_add(self.nei[self.nei[0][t]][4],-1)
                                self.exec_add(11,-1)
                                self.exec_add(self.nei[self.nei[0][t]][4],1)
                            
                        elif 6>i>0: #fall 3 #-->fall 2
                            #print ("6.3")
                            if j==0:
                                self.exec_add(self.nei[i][0],1)
                                self.exec_add(11,1)
                                self.exec_add(self.nei[i][0],-1)
                            #else:
                                #print("fault")

                            
        else:
            self.solve_mod+=1
            #self.set_skip=0

    def solve_7(self):
        t=5
        for i in range(5):
            if self.parts[self.nei[self.nei[0][i]][0]][1*2+1]!=self.muster[self.nei[self.nei[0][i]][0]][1*2+1]:
                if t==5:
                    t=i
        
        if t!=5:
            for i in range(12):
                for j in range(5):
                    if self.muster[self.nei[self.nei[0][t]][0]][1*2+1]==self.parts[i][j*2+1]:
                        if i == 11: #fall 1 #--> fall 2
                            #print ("7.1")
                            #nach links einsortieren
                            for B in range(5):
                                if self.nei[11][B]==self.nei[self.nei[0][t]][4]:
                                    b=B
                            self.move_ft(11,j,b)
                            
                            self.exec_add(11,1)
                            self.exec_add(11,1)
                            self.exec_add(self.nei[11][b],-1)
                            self.exec_add(self.nei[11][b],-1)
                            self.exec_add(11,1)
                            self.exec_add(11,1)
                            self.exec_add(self.nei[11][b],1)
                            self.exec_add(11,1)
                            self.exec_add(self.nei[11][b],-1)
                            self.exec_add(11,1)
                            self.exec_add(11,1)
                            self.exec_add(self.nei[11][b],1)
                            self.exec_add(self.nei[11][b],1)
                            
                            
                        elif 11>i>5: #fall 2 #main
                            if j == 2:#nach rechts einsortieren
                                #print ("7.2")
                                for A in range(5):
                                    if self.nei[11][A]==i:
                                        a=A
                                for B in range(5):
                                    if self.nei[11][B]==self.nei[self.nei[0][t]][0]:
                                        b=B
                                self.move_ft(11,a,b)
                                
                                self.exec_add(11,-1)
                                self.exec_add(11,-1)
                                self.exec_add(self.nei[11][b],1)
                                self.exec_add(self.nei[11][b],1)
                                self.exec_add(11,-1)
                                self.exec_add(11,-1)
                                self.exec_add(self.nei[11][b],-1)
                                self.exec_add(11,-1)
                                self.exec_add(self.nei[11][b],1)
                                self.exec_add(11,-1)
                                self.exec_add(11,-1)
                                self.exec_add(self.nei[11][b],-1)
                                self.exec_add(self.nei[11][b],-1)
                            else:
                                x=1
                                if j==3:
                                    x=-1
                                for B in range(5):
                                    if self.nei[11][B]==i:
                                        b=B
                                self.exec_add(self.nei[11][b],1*x)
                                self.exec_add(self.nei[11][b],1*x)
                                self.exec_add(11,-1*x)
                                self.exec_add(11,-1*x)
                                self.exec_add(self.nei[11][b],-1*x)
                                self.exec_add(11,-1*x)
                                self.exec_add(self.nei[11][b],1*x)
                                self.exec_add(11,-1*x)
                                self.exec_add(11,-1*x)
                                self.exec_add(self.nei[11][b],-1*x)
                                self.exec_add(self.nei[11][b],-1*x)
                            
        else:
            self.solve_mod+=1
            #print(self.moves)
            #self.set_skip=0

    def solve_8(self):
        t=5
        for i in range(5):
            if self.parts[11][i*2+1][0]!=self.muster[11][i*2+1][0]:
                if t==5:
                    t=i
        
        if t!=5:
            for j in range(5):
                if self.parts[11][j*2+1][0]!=self.muster[11][j*2+1][0] and j!=t:
                    n=(t-j)%5
                    if n in (1,2):
                        self.exec_add(self.nei[11][t],1)
                        self.exec_add(self.nei[self.nei[11][t]][3],1)
                        self.exec_add(11,1)
                        self.exec_add(self.nei[self.nei[11][t]][3],-1)
                        self.exec_add(11,-1)
                        self.exec_add(self.nei[11][t],-1)
                    else:
                        self.exec_add(self.nei[11][t],-1)
                        self.exec_add(self.nei[self.nei[11][t]][1],-1)
                        self.exec_add(11,-1)
                        self.exec_add(self.nei[self.nei[11][t]][1],1)
                        self.exec_add(11,1)
                        self.exec_add(self.nei[11][t],1)
                        
                    
                            
        else:
            self.solve_mod+=1
            #print(self.moves)
            #self.set_skip=0

    def solve_9(self):
        t=5
        for i in range(5):
            if self.parts[11][i*2+1]!=self.muster[11][i*2+1]:
                if t==5:
                    t=i

        if t!=5:
            for j in range(5):
                if self.parts[11][j*2+1]==self.muster[11][t*2+1]:
                    if t==0:
                        self.move_ft(11,j,t)
                    else:
                        n=(j-t)%5

                        if n==1:
                            self.exec_add(self.nei[11][t],-1)
                            self.exec_add(11,-1)
                            self.exec_add(11,-1)
                            self.exec_add(self.nei[11][t],1)
                            self.exec_add(11,1)
                            self.exec_add(self.nei[11][t],-1)
                            self.exec_add(11,1)
                            self.exec_add(self.nei[11][t],1)
                        elif n==2:
                            self.exec_add(self.nei[11][t],-1)
                            self.exec_add(11,-1)
                            self.exec_add(self.nei[11][t],1)
                            self.exec_add(11,-1)
                            self.exec_add(self.nei[11][t],-1)
                            self.exec_add(11,1)
                            self.exec_add(11,1)
                            self.exec_add(self.nei[11][t],1)
                        elif n==3:
                            self.exec_add(self.nei[11][t],-1)
                            self.exec_add(11,-1)
                            self.exec_add(11,-1)
                            self.exec_add(self.nei[11][t],1)
                            self.exec_add(11,-1)
                            self.exec_add(self.nei[11][t],-1)
                            self.exec_add(11,-1)
                            self.exec_add(11,-1)
                            self.exec_add(self.nei[11][t],1)
                                             
        else:
            self.solve_mod+=1
            #print(self.moves)
            #self.set_skip=0

    def solve_10(self):
        #a-->b
        a=0
        b=5
        for t in range(5):
            if b==5:
                p=0
                for i in range(12):
                    for j in range(5):
                        if self.parts[i][j*2]==self.muster[11][t*2]:
                            if i==11:
                                p=j
                            else:
                                for r in range(5):
                                    if  self.parts[self.nei[11][r]][3*2]==self.muster[11][t*2]:
                                        p=r
                                    elif self.parts[self.nei[11][r]][2*2]==self.muster[11][t*2]:
                                        p=(r+1)%5
                if t!=p:
                    a=p
                    b=t
        if b!=5:
            #print(a,b)
            
            n=(a-b)%5
            #print(n,b)
            
            if n == 1:
                self.exec_add(11,1)
                self.exec_add(self.nei[11][(b+2)%5],1)
                self.exec_add(11,-1)
                self.exec_add(11,-1)
                self.exec_add(self.nei[11][(b-1)%5],-1)
                self.exec_add(11,1)
                self.exec_add(11,1)
                self.exec_add(self.nei[11][(b+2)%5],-1)
                self.exec_add(11,-1)
                self.exec_add(11,-1)
                self.exec_add(self.nei[11][(b-1)%5],1)
                self.exec_add(11,1)
                
            elif n==2:
                self.exec_add(11,-1)
                self.exec_add(self.nei[11][(b-1)%5],-1)
                self.exec_add(11,1)
                self.exec_add(11,1)
                self.exec_add(self.nei[11][(b+2)%5],1)
                self.exec_add(11,-1)
                self.exec_add(11,-1)
                self.exec_add(self.nei[11][(b-1)%5],1)
                self.exec_add(11,1)
                self.exec_add(11,1)
                self.exec_add(self.nei[11][(b+2)%5],-1)
                self.exec_add(11,-1)
                
            elif n==3:
                self.exec_add(11,1)
                self.exec_add(self.nei[11][(b-2)%5],1)
                self.exec_add(11,-1)
                self.exec_add(11,-1)
                self.exec_add(self.nei[11][(b)%5],-1)
                self.exec_add(11,1)
                self.exec_add(11,1)
                self.exec_add(self.nei[11][(b-2)%5],-1)
                self.exec_add(11,-1)
                self.exec_add(11,-1)
                self.exec_add(self.nei[11][(b)%5],1)
                self.exec_add(11,1)
                
            elif n==4:
                self.exec_add(11,-1)
                self.exec_add(self.nei[11][(b+1)%5],-1)
                self.exec_add(11,1)
                self.exec_add(11,1)
                self.exec_add(self.nei[11][(b-1)%5],1)
                self.exec_add(11,-1)
                self.exec_add(11,-1)
                self.exec_add(self.nei[11][(b+1)%5],1)
                self.exec_add(11,1)
                self.exec_add(11,1)
                self.exec_add(self.nei[11][(b-1)%5],-1)
                self.exec_add(11,-1)
        else:
            self.solve_mod+=1
            #print(self.moves)
            #self.set_skip=0

    def solve_11(self):
        t=5
        for i in range(5):
            if self.parts[11][i*2]!=self.muster[11][i*2]:
                if t==5:
                    t=i

        if t!=5:
            #print(t)
            self.move_ft(11,t,0)

            self.exec_add(self.nei[self.nei[11][0]][3],-1)
            self.exec_add(self.nei[self.nei[11][0]][4],-1)
            self.exec_add(self.nei[self.nei[11][0]][3],1)
            self.exec_add(self.nei[self.nei[11][0]][4],1)
            
            self.move_ft(11,0,t)

        else:
            #print("SOLVED("+str(self.moves)+")")
            self.desolve()
            
    def move_ft(self,i,a,b):
        n=b-a
        n=(n+2)%5-2
        if n>0:
            for k in range(n):
                self.exec_add(i,1)
        elif n<0:
            for k in range(-n):
                self.exec_add(i,-1)
    
                        

    def tick(self):
        x=1
        while x:
            x=0
            if self.skip==1 and self.exec_f==1:
                x=1

            if self.roll==0:
                if self.exec_f==1:
                    if len(self.exec_list)==0:
                        self.exec_f=0
            
            if self.mod==2:
                if self.exec_f==0:
                    exec("self.solve_"+str(self.solve_mod)+"()")
                    
             #Auto executer
            if self.roll==0:
                if self.exec_f==1:
                    self.skip=self.set_skip
                    self.execute()

            #Auto Dreher
            if (self.roll != 0):
                if self.skip==0:
                    q=8
                    self.rollv[2]=self.rollv[2]+self.rollv[1]*q
                    if -72< self.rollv[2] < 72:
                        self.rollen(self.rollv[0],self.rollv[1]*q)
                        
                    else:
                        self.rollen(self.rollv[0],-self.rollv[2]+self.rollv[1]*q)
                        self.spin(self.rollv[0],self.rollv[1])
                        self.rollv=[0,0,0]
                        self.roll=0
                        self.black=[]
                else:
                    self.spin(self.rollv[0],self.rollv[1])
                    self.rollv=[0,0,0]
                    self.roll=0
                    self.black=[]

    def back(self):
        if len(self.reset)>0:
            self.desolve()
            self.reset_f=1
            res=len(self.reset)-1
            self.exec_list.append((self.reset[res][0],-self.reset[res][1]))
            self.exec_f=1
            self.reset=self.reset[:res]
        else:
            pass
            #print("CANT REMEMBER")

    def execute(self):
        if len(self.exec_list)==0:
            self.exec_f=0
            print("no commands for execute")
        else:
            self.drehen(self.exec_list[0][0],self.exec_list[0][1])
            if self.reset_f==0:
                self.reset.append(self.exec_list[0])
                if len(self.reset)>1000:
                    self.reset=self.reset[1:]
            self.reset_f=0
            if len(self.exec_list)==1:
                self.exec_list = []
                if self.mod == 1:
                    self.mod = 0

                
            else:
                self.exec_list=self.exec_list[1:]

    def drehen(self,i,x):
        #intaliserung zum drehen einer seite
        if self.roll==0:
            self.roll=1
            self.rollv=[i,x,0]
            self.black.append([
                self.parts_p[i][j*2][2][3] for j in range(5)
                ])
            self.black.append([
                self.blackp[i][j][2] for j in range(5)
                ])    

    def strukture(self):

        #farben der teilflächen der seiten
        self.seiten = [[[i]for j in range(11)]for i in range(12)]
        #self.seiten[1][0][0]=8
        #self.seiten[7][0][0]=2
        #self.seiten[8][0][0]=3


        #==============================================================
        L=[]#für alle seiten (anliegende seiten,nummer dieser)
        for i in range(12):
            if i==0:
                L.append(  (  (1,2,3,4,5),
                              (5,5,5,5,5)  )  )
            elif i==11:
                L.append(  (  (6,7,8,9,10),
                              (5,5,5,5,5)  )  )
            elif i<6:
                L.append(  (  ((2-i)%5+6,i%5+1,0,(i-2)%5+1,(3-i)%5+6),
                              (1,7,(i-1)*2+1,3,9)  )  )
            else:
                L.append(  (  ((2-i)%5+1,i%5+6,11,(i-2)%5+6,(3-i)%5+1),
                              (1,7,(i-6)*2+1,3,9)  )  )

        self.nei=[L[i][0] for i in range(12)]
        
        self.parts=[]
        for i in range(12):
            LIST=[]
            for j in range(5):
                LIST.append(
                    [
                        self.seiten[i][j*2],
                        self.seiten[ L[i][0][(j+4)%5] ][( L[i][1][(j+4)%5] -1)%10],
                        self.seiten[ L[i][0][j] ][( L[i][1][j] +1)%10]
                        ]
                    )#ecke
                LIST.append(
                    [
                        self.seiten[i][(j*2+1)%10],
                        self.seiten[ L[i][0][j] ][ L[i][1][j] ]
                        ]
                    )
            self.parts.append(LIST)
            
        self.parts_p=[]
        for i in range(12):
            LIST=[]
            for j in range(5):
                LIST.append(
                    [
                        self.polygons[i][j*2],
                        self.polygons[ L[i][0][(j+4)%5] ][( L[i][1][(j+4)%5] -1)%10],
                        self.polygons[ L[i][0][j] ][( L[i][1][j] +1)%10]
                        ]
                    )#ecke
                LIST.append(
                    [
                        self.polygons[i][(j*2+1)%10],
                        self.polygons[ L[i][0][j] ][ L[i][1][j] ]
                        ]
                    )
            LIST.append([self.polygons[i][10]])
            self.parts_p.append(LIST)

        self.blackp=[] # flächen für schwarze flächen
        for i in range(12):
            LIST=[]
            for j in range(5):
                LIST.append(self.polygons[ L[i][0][(j+4)%5] ][( L[i][1][(j+4)%5] -2)%10])
            self.blackp.append(LIST)
            

    def muster(self):
        self.muster=[
            [
                [
                    [self.parts[i][j][k][0]]for k in range(len(self.parts[i][j]))
                    ]for j in range(10)
                ]for i in range(12)
            ]
        
    #=======================================================================================
    #RESOURES===============================================================================
    #=======================================================================================
            
    def spin(self,i,x):
        #verschiebt die farben der parts einer seite
        x=-x
        #oben
        parts=[self.parts[i][(x*2+j)%10][0][0] for j in range(10)]
        for j in range(10):
            self.parts[i][j][0][0]=parts[j]

        #erste
        parts=[self.parts[i][(x*2+j)%10][1][0] for j in range(10)]
        for j in range(10):
            self.parts[i][j][1][0]=parts[j]

        parts=[self.parts[i][(x*2+j*2)%10][2][0] for j in range(5)]
        for j in range(5):
            self.parts[i][j*2][2][0]=parts[j]

    def rollen(self,i,a):
        #dreht die farben der parts einer seite
        for part in self.parts_p[i]:
            for pol in part:
                for p in pol:
                    p.turn(0,0,0,0,-self.yaw[i],0)
                    p.turn(0,0,0,-self.pitch[i],0,0)
                    p.turn(0,0,0,0,a,0)
                    p.turn(0,0,0,self.pitch[i],0,0)
                    p.turn(0,0,0,0,self.yaw[i],0) 

    def radius(self):
        #errechnet entfernug vom megaminx.mittelpunkt zum seite.mittelpunkt 
        sr = 3-2*m.sin(18*s.grad)
        a= m.cos(54*s.grad)*sr*2
        r=a/2*m.sqrt((25+11*m.sqrt(5))/10)
        return r

    def create(self):
        
        self.pitch=[0 for i in range(12)]
        self.yaw=[0 for i in range(12)]
        
        for i in range(5):
            self.pitch[i+1]=180-self.FFW
            self.yaw[i+1]=36+72*i
        for i in range(5):
            self.pitch[i+6]=-self.FFW
            self.yaw[i+6]=72*((-i-0.5)%5)
        self.pitch[11]=180
        self.yaw[11]=0

        pol=[
            self.Seite(0,
                                  self.r,#+0.015,
                                  0,
                                  self.pitch[i],
                                  self.yaw[i]
                       )for i in range(12)
            ]
        
        return pol

    
    def colors(self):
        self.color=[
            (0.9,0.9,0.9),
            
            (0.15,0.15,0.15),
            (1.0,0.6,0.0),
            (0.4,0.4,1.0),
            (0.7,0.0,0.8),
            (0.0,0.3,0.0),
            
            (0.0,0.6,0.0),
            (1.0,0.6,0.8),
            (0.0,0.0,0.45),
            (0.5,0.0,0.0),
            (0.5,0.5,0.5),
            
            (0.9,0.9,0.0)
            ]

    def Seitea(self):
        main=[
            P.Point(
                m.cos((72*i-90)*s.grad),
                0,
                m.sin((72*i-90)*s.grad)
                )for i in range(5)
            ]
        
        vertex=[
            P.Point(#innen
                0,
                0,
                m.sin((72*0-90)*s.grad)
                ),
            P.Point(#links
                m.cos((72*4-90)*s.grad),
                0,
                m.sin((72*0-90)*s.grad)*2 - m.sin((72*1-90)*s.grad)
                ),
            P.Point(#außen
                0,
                0,
                m.sin((72*0-90)*s.grad)*3 - 2*(m.sin((72*1-90)*s.grad))
                ),
            P.Point(#rechts
                m.cos((72*1-90)*s.grad),
                0,
                m.sin((72*0-90)*s.grad)*2 - m.sin((72*1-90)*s.grad)
                )
            ]
        
        vertices=[0 for i in range(5)]
        for i in range(4):
            vertices[i]=[
                P.Point(
                    vertex[j].x,
                    vertex[j].y,
                    vertex[j].z
                    )for j in range(4)
                ]
            
            for p in vertex:
                p.turn(0,0,0, 0,72,0)
                
        vertices[4]=vertex

        edges=[0 for i in range(5)]
        for i in range(5):
            edges[i]=[
                P.Point(
                    vertices[i][0].x,
                    vertices[i][0].y,
                    vertices[i][0].z
                    ),
                P.Point(
                    vertices[i][3].x,
                    vertices[i][3].y,
                    vertices[i][3].z
                    ),
                P.Point(
                    vertices[(i+1)%5][1].x,
                    vertices[(i+1)%5][1].y,
                    vertices[(i+1)%5][1].z
                    ),
                P.Point(
                    vertices[(i+1)%5][0].x,
                    vertices[(i+1)%5][0].y,
                    vertices[(i+1)%5][0].z
                    ),
                ]
            
        return [
            vertices[0],edges[0],
            vertices[1],edges[1],
            vertices[2],edges[2],
            vertices[3],edges[3],
            vertices[4],edges[4],
            main
            ]

    
    def Seite(self,x,y,z,pitch,yaw):
        Seite=self.Seitea()
        for area in Seite:
            for p in area:
                p.move(x,y,z)
                p.turn(0,0,0,pitch,0,0)
                p.turn(0,0,0,0,yaw,0)
                #p.move(x,y,z)

        return Seite





if __name__=="__main__":
    import MAIN















