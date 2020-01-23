import time
import numpy as np
import pickle
import CoordTrans

foils = {
    0: 'Blank',
    1: 'Fluorescent',
    2: 'Calibration',
    3: 'Ti1',
    4: 'Ti2',
    5: 'Ti3',
    6: 'Ti4',
    7: 'Cross'
}


# Generic Foil class, common among all Foils:
class Foil:
    def __init__(self, ID=1, normal=np.array([[0, 1, 0]]), diam=50.):
        self.ID = ID
        self.diam = diam
        self.normal = normal

    def GetID(self):
        return self.ID

    def GetType(self):
        return foils[self.ID]

    def GetDiameter(self):
        return self.diam

    def PlaneIntersect(self, X, V):
        y = X[1]     # selects the y component of all rays
        Vy = V[1]    # selects the vy component of all rays
        eps = 10e-5  # tolerance
        Y = 0.       # Position of Foil Plane in Foil Reference System
        AtPlane = np.abs(y - Y) > eps
        HasV = np.abs(Vy) > eps
        GoodRays = np.logical_and(AtPlane, HasV)
        y = y[GoodRays]
        Vy = Vy[GoodRays]
        X = X.T[GoodRays] 
        V = V.T[GoodRays]
        # Only keep rays that are pointing at the foil:
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
        passed = np.diag(Xint.T.dot(Xint)) < (self.diam**2) / 4.
        Xint = Xint.T[passed]
        V = V.T[passed]
        return Xint.T, V.T

    def PlaneReflect(self, V):
        return V - 2 * self.normal.dot(V) * self.normal.T

    def PlaneTransport(self, X, V):
        X, V = self.PlaneIntersect(X, V)
        return X, self.PlaneReflect(V)


# Calibration Foil class, inherits from Generic Foil class:
# class CalibrationFoil(OpticalComponent, Foil):
class CalibrationFoil(Foil):
    def __init__(self, hole_dist=7., hole_diam=1.2,
                 normal=np.array([[0., 1., 0.]]), diam=55., epsilon_dia=0):
        # OpticalComponent.__init__(self)
        Foil.__init__(self, ID=2, normal=normal, diam=diam)
        self.fName = self.GetType()
        self.fHdist = hole_dist
        self.fHdmtr = hole_diam
        self.holes = self.MakeHoles()

    def MakeHoles(self):
        import os, sys, pickle
        sys.path.append('macros')
        from MakeCalibHoles import MakeHoles
        calib_pickle = 'data/calib_holes.p'
        if os.path.isfile(calib_pickle):
            return pickle.load(open(calib_pickle, 'rb'))
        return MakeHoles()

    def PrintHolePos(self, screen=False):
        print('Using Calibration Holes:')
        for i, ihole in enumerate(self.holes):
            print('{0} {1} {2}'.format(i, ihole[0], ihole[2]))

    def PassHole(self, X):
        masks = []
        for ihole in self.holes:
            ihole = np.array(ihole)
            diff = X - ihole[:-1].reshape(3, 1)
            mask = np.diag(diff.T.dot(diff)) < (ihole[-1]**2) / 4.
            masks.append(mask)
        passed = np.array([False] * len(masks[0]))
        for mask in masks:
            passed = np.logical_or(passed, mask)
        return passed

    def RaysTransport(self, X, V):
        euler = np.array([0., np.pi / 2, 0.])
        fTrCoord = CoordTrans.CoordTrans(X=np.zeros((1, 3)), angles=euler)
        # Go to local coords:
        X = fTrCoord.TransfrmPoint(X)
        V = fTrCoord.TransfrmVec(V)
        # Get X interaction points and V reflected:
        Xint, Vr = self.PlaneTransport(X, V)
        passed = self.PassHole(Xint)
        Vr = np.array([v if p else vr
                       for p, v, vr in zip(passed, V.T, Vr.T)]).T
        # Transform back to the global coords:
        Xint = fTrCoord.TransfrmPoint(Xint, inv=True)
        Vr = fTrCoord.TransfrmVec(Vr, inv=True)
        return Xint, Vr
