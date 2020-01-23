import numpy as np
from numpy import cos, sin, pi


class CoordTrans():
    def __init__(self, X=np.zeros((1, 3)), angles=np.zeros(3)): 
        # angles = phi, theta, psi
        self.X = X
        self.angles = angles
        self.M = self.GetM()

    def Reset(self):
        self.X = np.zeros((1, 3))
        self.angles = np.zeros(3)
        self.M = self.GetM()

    def SetPosition(self, X):
        self.X = X

    def SetOrientation(self, angles):
        self.angles = angles
        self.M = self.GetM()

    def GetM(self):        
        phi, theta, psi = self.angles
        # Rotation of phi around z
        R1 = np.array([[cos(phi), sin(phi), 0],
                       [-sin(phi), cos(phi), 0],
                       [0, 0, 1]])
        # Rotation of theta around x_prime 
        R2 = np.array([[1, 0, 0],
                       [0, cos(theta), sin(theta)],
                       [0, -sin(theta), cos(theta)]])
        # Rotation of psi around z_2primes
        R3 = np.array([[cos(psi), sin(psi), 0],
                       [-sin(psi), cos(psi), 0],
                       [0, 0, 1]])
        return R3.dot(R2.dot(R1))

    def DoPointTrans(self, points, inv=False):
        return points + self.X.T if inv else points - self.X

    def DoPointRot(self, points, inv=False):
        return self.M.T.dot(points) if inv else self.M.dot(points.T)

    def TransfrmPoint(self, points, inv=False):
        if inv:
            return self.DoPointTrans(self.DoPointRot(points, inv=True), inv=True)
        return self.DoPointRot(self.DoPointTrans(points))

    def TransfrmVec(self, V, inv=False):
        return self.DoPointRot(V, inv)
