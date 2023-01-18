import numpy as np
from tqdm import tqdm

def force(m1,X1,m2,X2) :
    G=4*np.pi**2    
    d=np.linalg.norm(X1-X2)
    f=-(G*m1*m2/(d**3))*(X1-X2)
    return f
    


class Resolution:
    def __init__(self, y, t0, tf, N, nb_corps, M, state_rebond, teta_list):
        self.y = y
        self.t0 = t0
        self.tf = tf
        self.N = N
        self.nb_corps = nb_corps
        self.M = M
        self.state_rebond = state_rebond
        self.teta_list = teta_list
        self.h = (tf-t0)/N
    
    def f(self, t, y, M):
        nb_corps=len(M)
        F=np.zeros((nb_corps*6,1))
        for i in range(nb_corps) :
            S=np.zeros((3,1))
            for j in range(nb_corps) : 
                if j != i:
                    S+=force(M[i], y[i*3:(i+1)*3,0].reshape(-1,1),M[j],y[j*3:(j+1)*3,0].reshape(-1,1))
                
            F[i*3:(i+1)*3,0]=y[nb_corps*3+i*3:(i+1)*3+nb_corps*3,0]  
            F[nb_corps*3+i*3:(i+1)*3+nb_corps*3,0]=(1/M[i]*S).reshape(-1)    
        return F   

    
    def RK2(self):
        t = self.t0
        Y = np.zeros((3*self.nb_corps, self.N))
        for i in tqdm(range(0, self.N)):
            k1 = self.h * self.f(t, self.y, self.M)
            k2 = self.h * self.f(t + self.h, self.y + k1, self.M)
            self.y = self.y + (k1 + k2) / 2
            t += self.h
            for j in range(0, self.nb_corps):
                Y[j*3:(j+1)*3, i] = self.y[j*3:(j+1)*3, 0]
            for j in range(0, self.nb_corps-1):
                for i in range(1, self.nb_corps):  
                    if j != i: 
                        X1 = self.y[j*3:(j+1)*3, 0].reshape(-1, 1) 
                        X2 = self.y[i*3:(i+1)*3, 0].reshape(-1, 1)
                        distance = np.linalg.norm(X1-X2)
                        if distance < 4 and self.state_rebond == 1: 
                            self.y[3*(self.nb_corps+j):3*(self.nb_corps+j+1), 0] = -self.y[3*(self.nb_corps+j):3*(self.nb_corps+j+1), 0]
                            self.y[3*(self.nb_corps+i):3*(self.nb_corps+i+1), 0] = -self.y[3*(self.nb_corps+i):3*(self.nb_corps+i+1), 0]
        return Y
    
    def RK4(self):
        t= self.t0
        Y= np.zeros((3*self.nb_corps, self.N))
        for i in tqdm(range(0,self.N)) : 
            k1=self.h*self.f(t,self.y,self.M)
            k2=self.h*self.f(t+self.h/2, self.y+k1/2,self.M)
            k3=self.h*self.f(t+self.h/2, self.y+k2/2,self.M)
            k4=self.h*self.f(t+self.h, self.y+k3,self.M)
            self.y=self.y+(1/6)*(k1 +2*k2 +2*k3 + k4)
            t+=self.h    
            for j in range(0,self.nb_corps) :
                Y[j*3:(j+1)*3,i]=self.y[j*3:(j+1)*3,0]
            for j in range(0,self.nb_corps-1):
                for i in range(1,self.nb_corps):  
                    if j!=i: 
                        X1=self.y[j*3:(j+1)*3,0].reshape(-1,1) 
                        X2=self.y[i*3:(i+1)*3,0].reshape(-1,1)
                        distance=np.linalg.norm(X1-X2)
                        if  distance<4 and self.state_rebond==1: 
                            self.y[3*(self.nb_corps+j):3*(self.nb_corps+j+1),0]=-self.y[3*(self.nb_corps+j):3*(self.nb_corps+j+1),0]
                            self.y[3*(self.nb_corps+i):3*(self.nb_corps+i+1),0]=-self.y[3*(self.nb_corps+i):3*(self.nb_corps+i+1),0]
        return(Y)   
    
    def RK45(self):
        t=self.t0
        ErreurAdmis=1e-6
        Y=np.zeros((3*self.nb_corps,self.N))
        for i in tqdm(range(0,self.N)) : 
            k1 = self.f(t, self.y, self.M)
            k2 = self.f(t+self.h/5, self.y+self.h*k1/5, self.M)
            k3 = self.f(t+3*self.h/10, self.y+3*self.h*(k1+3*k2)/40, self.M)
            k4 = self.f(t+3*self.h/5, self.y+self.h*((k1*3/10)-(k2*9/10)+(k3*6/5)), self.M)
            k5 = self.f(t+self.h, self.y+self.h*((-k1*11/54)+(k2*5/2)-(k3*70/27)+(k4*35/27)), self.M)
            k6 = self.f(t+self.h*7/8, self.y+self.h*((k1*1631/55296)+(k2*175/512)+(k3*575/13824)+(k4*44275/110592)+(k5*253/4096)), self.M)
            t+=self.h    
            ya=self.y+np.array(self.h*(37*k1/378+250*k3/621+125*k4/594+512*k6/1771))
            yb=self.y+np.array(self.h*(2825*k1/27648+18575*k3/48384+13525*k4/55296+277*k5/14336+k6/4))
            ErreurActuel=np.linalg.norm(np.abs(ya-yb))
            if (ErreurAdmis<=ErreurActuel):
                self.h=self.h*(ErreurAdmis/ErreurActuel)**0.2
            if (ErreurAdmis>ErreurActuel and ErreurActuel>0.0):
                self.h=self.h*(ErreurAdmis/ErreurActuel)**0.25
            if (self.h>(self.tf-self.t0)/self.N):
                self.h=(self.tf-self.t0)/self.N     
            for j in range(0,self.nb_corps):
                Y[j*3:(j+1)*3,i]=yb[j*3:(j+1)*3,0] 
            self.y=yb    
            if self.h<1e-6:
                self.h=1e-6
            for j in range(0,self.nb_corps-1):
                for i in range(1,self.nb_corps):  
                    if j!=i: 
                        X1=self.y[j*3:(j+1)*3,0].reshape(-1,1) 
                        X2=self.y[i*3:(i+1)*3,0].reshape(-1,1)
                        distance=np.linalg.norm(X1-X2)
                        if  distance<4 and self.state_rebond==1: 
                            self.y[3*(self.nb_corps+j):3*(self.nb_corps+j+1),0]=-self.y[3*(self.nb_corps+j):3*(self.nb_corps+j+1),0]
                            self.y[3*(self.nb_corps+i):3*(self.nb_corps+i+1),0]=-self.y[3*(self.nb_corps+i):3*(self.nb_corps+i+1),0]          
        return Y



