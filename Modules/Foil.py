import numpy as np
from OpticalComponent import OpticalComponent


# Generic Foil class, common among all Foils:
class Foil(OpticalComponent):
    def __init__(self, normal=np.array([[0, 1, 0]]), diam=50., name=None):
        OpticalComponent.__init__(self, name=name)
        self.diam = diam
        self.normal = normal

    def PlaneIntersect(self, X, V):
        y = X[:, 1]     # selects the y component of all rays
        Vy = V[:, 1]    # selects the vy component of all rays
        eps = 10e-5  # tolerance
        Y = 0.       # Position of Foil Plane in Foil Reference System
        AtPlane = np.abs(y - Y) > eps
        HasV = np.abs(Vy) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        y = y[GoodRays]
        Vy = Vy[GoodRays]
        X = X[GoodRays]
        V = V[GoodRays]
        # Only keep rays that are pointing at the foil:
        ToPlane = Vy / np.abs(Vy) != (y - Y) / np.abs(y - Y)
        y = y[ToPlane]
        Vy = Vy[ToPlane]
        X = X[ToPlane]
        V = V[ToPlane]
        # interaction at y = 0, by construction:
        t = (Y - y) / Vy
        assert (t > 0).all()
        t.resize(t.shape[0], 1)
        Xint = X + V * t
        assert (np.abs(Xint[:, 1] - Y) < eps).all()
        # Only keep rays that cross the Foil:
        passed = np.diag(Xint.dot(Xint.T)) < (self.diam**2) / 4.
        Xint = Xint[passed]
        V = V[passed]
        assert Xint.shape == V.shape
        return Xint, V

    def PlaneReflect(self, V):
        return V - 2 * V.dot(self.normal.T) * self.normal

    def PlaneTransport(self, X, V):
        X, V = self.PlaneIntersect(X, V)
        return X, self.PlaneReflect(V)


# Calibration Foil class, inherits from Generic Foil class:
# class CalibrationFoil(OpticalComponent, Foil):
class CalibrationFoil(Foil):
    def __init__(self, normal=np.array([[0., 1., 0.]]), diam=50.,
                 hole_dist=7., hole_diam=1.2, name=None):
        Foil.__init__(self, normal=normal, diam=diam)
        self.hole_dist = hole_dist
        self.hole_diam = hole_diam
        self.holes = self.GetHoles()

    def GetHoles(self):
        import os
        from MakeCalibHoles import MakeHoles
        calibfile = 'data/calib_holes.npy'
        if os.path.isfile(calibfile):
            return np.load(calibfile)
        return MakeHoles(fHdist=self.hole_dist, fHdmtr=self.hole_diam)

    def PrintHolePos(self, screen=False):
        print('Using Calibration Holes:')
        for i, ihole in enumerate(self.holes):
            print('{0} {1} {2}'.format(i, ihole[0], ihole[2]))

    def PassHole(self, X):
        masks = []
        for ihole in self.holes:
            diff = X - ihole[:-1].reshape(1, 3)
            mask = np.diag(diff.dot(diff.T)) < (ihole[-1]**2) / 4.
            masks.append(mask)
        passed = np.array([False] * len(masks[0]))
        for mask in masks:
            passed = np.logical_or(passed, mask)
        return passed

    def RaysTransport(self, X, V):
        # Go to local coords:
        X = self.transform_coord.TransfrmPoint(X)
        V = self.transform_coord.TransfrmVec(V)
        # Get X interaction points and V reflected:
        Xint, Vr = self.PlaneTransport(X, V)
        passed = self.PassHole(Xint)
        Vr = np.array([v if p else vr
                       for p, v, vr in zip(passed, V, Vr)])
        # Transform back to the global coords:
        Xint = self.transform_coord.TransfrmPoint(Xint, inv=True)
        Vr = self.transform_coord.TransfrmVec(Vr, inv=True)
        return Xint, Vr
