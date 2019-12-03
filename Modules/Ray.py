import numpy as np

class Ray:
      def __init__(self, X=np.array([1., 1., -1.]), V=np.array([0., 0., 1.])):
          self.X = X
          self.V = V
      def SetPosition(self, X): self.X = X
      def SetDirection(self, V): self.V = V
      def GetPosition(self): return self.X
      def GetDirection(self): return self.V

      def ZPlaneIntersect(self, Z=0.):
          z = self.X[2]
          vz = self.V[2]
          if np.abs(z-Z) < 10e-9 or  np.abs(vz) < 10e-9: return False, 0          
          if vz/np.abs(vz) ==  (z-Z)/np.abs(z-Z): return False, 0
          t = 1.*(Z - z) / vz
          assert t >= 0.
          pos_int = self.X + self.V*t
          assert np.abs(pos_int[2] - Z) < 10e-9
          return True, pos_int
