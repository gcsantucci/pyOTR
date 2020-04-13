import numpy as np


class Mirror:
      def __init__(self):
            pass


class ParaMirror(Mirror):
      def __init__(self, f, H, D, rough=False):
            self.f = f  # focal length
            self.H = H  # Height
            self.D = D  # Diameter
            self.rough = rough  # simulate roughness?
            self.seed = 42
            self.shift = np.array([[2. * self.f, self.f, 0]])

      def Shift(self, X):
            return X + self.shift

      def F_mirror(self, t, X, V):
            Xr = X + (V * t)
            Xp = np.array([Xr[0], 4. * self.f, Xr[2]])  # maybe .T
            return Xr.dot(Xp)

      def Fprime_mirror(self, t, X, V):
