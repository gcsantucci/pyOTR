import numpy as np
from numpy import cos, sin, pi

class CoordTrans():
    def __init__(self, X=np.zeros(3), angles=np.zeros(3)): #angles = phi, theta, psi
        self.X = X
        self.angles = angles
        self.M = self.GetM()

    def Reset(self):
        self.X = np.zeros(3)
        self.angles = np.zeros(3)
        self.M = self.GetM()

    def SetPosition(self, X): self.X = X
    def SetOrientation(self, angles):
        self.angles = angles        
        self.M = self.GetM()

    def GetM(self):
        phi, theta, psi = self.angles
        R1 = np.array([[cos(phi), sin(phi), 0],        #Rotation of phi around z 
                       [-sin(phi), cos(phi), 0],
                       [0, 0, 1]])
        R2 = np.array([[1, 0, 0],                      #Rotation of theta around x_prime  
                       [0, cos(theta), sin(theta)],
                       [0, -sin(theta), cos(theta)]])
        R3 = np.array([[cos(psi), sin(psi), 0],       #Rotation of psi around z_2primes 
                       [-sin(psi), cos(psi), 0],
                       [0, 0, 1]])
        M = R3.dot(R2.dot(R1))
        return M

    def DoPointTrans(self, point, inv=False): return point + self.X if inv else point - self.X
    def DoPointRot(self, point, inv=False): return self.M.T.dot(point) if inv else self.M.dot(point)
    
    def TransfrmPoint(self, point, inv=False):
        if not inv: return self.DoPointRot( self.DoPointTrans(point) )
        return self.DoPointTrans(self.DoPointRot(point, inv=True), inv=True)

    def TransfrmVec(self, V, inv=False):
        return self.DoPointRot(V, inv)
