import numpy as np
import CoordTrans

class OpticalComponent:
    def __init__(self, name=None):
        self.name = name

    def SetName(self, name):
        self.name = name

    def GetName(self):
        return self.name

    def GetPosition(self):
        return self.X

    def GetOrientation(self):
        return self.angles

    def Place(self, X=np.zeros((1, 3)), angles=np.zeros(3)):
        self.X = X
        self.angles = angles
        self.transform_coord = CoordTrans.CoordTrans(X=self.X, angles=self.angles)

