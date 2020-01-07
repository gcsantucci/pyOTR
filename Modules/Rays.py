import numpy as np

class Rays:
    def __init__(self, X=np.array([1., 1., -1.]), V=np.array([0., 0., 1.])):
        self.X = X
        self.V = V
    def SetPosition(self, X): self.X = X
    def SetDirection(self, V): self.V = V
    def GetPosition(self): return self.X
    def GetDirection(self): return self.V
    def MatrixIntersect(self, Z=0.):
        #assumes self is a 3xn Matrix with the x,y,z of n rays in each column    
        z = self.X[2] #selects the z component of all rays              
        Vz = self.V[2] #selects the vz component of all rays       
        eps = 10e-9 #tolerance     
        # see if it is better to save time or memory by using these AtPlane and HasV variables
        AtPlane = np.abs( z - Z ) > eps #optional: < eps and negate with ~ 
        HasV = np.abs(Vz) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        z = z[GoodRays]; Vz = Vz[GoodRays]
        X = self.X.T[GoodRays]; V = self.V.T[GoodRays]
        # check if velocity is pointing towards the plane or away from it: 
        #ToPlane = ~( v/np.abs(v) == (h-Z) / np.abs(h-Z) ) or:           
        ToPlane = Vz/np.abs(Vz) != (Z-z)/np.abs(Z-z)
        z = z[ToPlane]; Vz = Vz[ToPlane]
        X = X[ToPlane].T; V = V[ToPlane]
        #Remaining rays point to plane and will intersect it: 
        t = (Z - z) / Vz
        assert (t > 0).all()
        pos_int = X + V*t
        assert (np.abs(pos_int[2] - Z) < 10e-9).all()
        return pos_int

