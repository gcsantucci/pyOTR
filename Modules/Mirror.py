import numpy as np
from OpticalComponent import OpticalComponent


class Mirror:
    def __init__(self):
        pass


class PlaneMirror(Mirror, OpticalComponent):
    def __init__(self, normal=np.array([[0., 0., -1.]]), R=20.):
        self.name = 'PlaneMirror'
        self.normal = normal
        self.R = R

    def PlaneIntersect(self, X, V):
        z = X[:, 2]     # selects the z component of all rays
        Vz = V[:, 2]    # selects the Vz component of all rays
        eps = 10e-5  # tolerance
        Z = 0.       # Position of Mirror Plane in Mirror Reference System
        AtPlane = np.abs(z - Z) > eps
        HasV = np.abs(Vz) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        z = z[GoodRays]
        Vz = Vz[GoodRays]
        X = X[GoodRays]
        V = V[GoodRays]
        # Only keep rays that are pointing at the mirror:
        ToPlane = Vz / np.abs(Vz) != (z - Z) / np.abs(z - Z)
        z = z[ToPlane]
        Vz = Vz[ToPlane]
        X = X[ToPlane]
        V = V[ToPlane]
        # interaction at z = 0, by construction:
        t = (Z - z) / Vz
        assert (t > 0).all()
        t.resize(t.shape[0], 1)
        Xint = X + V * t
        assert (np.abs(Xint[:, 2] - Z) < eps).all()
        # Only keep rays that cross the Mirror:
        passed = np.diag(Xint.dot(Xint.T)) < (self.R**2)
        Xint = Xint[passed]
        V = V[passed]
        assert Xint.shape == V.shape
        return Xint, V

    def PlaneReflect(self, V):
        return V - 2 * V.dot(self.normal.T) * self.normal

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
