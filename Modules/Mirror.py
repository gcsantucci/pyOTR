import numpy as np
from OpticalComponent import OpticalComponent


class Mirror:
    def __init__(self):
        pass


class PlaneMirror(Mirror, OpticalComponent):
    def __init__(self, R=20.):
        self.name = 'PlaneMirror'
        self.R = R

    def PlaneIntersect(self, X, V):
        y = X[1]     # selects the y component of all rays
        Vy = V[1]    # selects the vy component of all rays
        eps = 10e-5  # tolerance
        Y = 0.       # Position of Mirror Plane in Mirror Reference System
        AtPlane = np.abs(y - Y) > eps
        HasV = np.abs(Vy) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        y = y[GoodRays]
        Vy = Vy[GoodRays]
        X = X.T[GoodRays]
        V = V.T[GoodRays]
        # Only keep rays that are pointing at the mirror:
        ToPlane = Vy / np.abs(Vy) != (y - Y) / np.abs(y - Y)
        y = y[ToPlane]
        Vy = Vy[ToPlane]
        X = X[ToPlane].T
        V = V[ToPlane].T
        # interaction at y = 0, by construction:
        t = (Y - y) / Vy
        assert (t > 0).all()
        Xint = X + V * t
        assert (np.abs(Xint[1] - Y) < eps).all()
        # Only keep rays that cross the Foil:
        passed = np.diag(Xint.T.dot(Xint)) < (self.R**2)
        Xint = Xint.T[passed]
        V = V.T[passed]
        return Xint.T, V.T

    def PlaneReflect(self, V):
        return V - 2 * self.normal.dot(V) * self.normal.T

    def PlaneTransport(self, X, V):
        X, V = self.PlaneIntersect(X, V)
        return X, self.PlaneReflect(V)

    def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get X interaction points and V reflected:
        Xint, Vr = self.PlaneTransport(X, V)
        # Transform back to the global coords:
        Xint = self.transform_coord.TransfrmPoint(Xint, inv=True)
        Vr = self.transform_coord.TransfrmVec(Vr, inv=True)
        return Xint, Vr


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
            pass
