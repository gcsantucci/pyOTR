import numpy as np
import CoordTrans

class OpticalComponent:
    def __init__(self):
        self.X = np.zeros(3)
        self.angles = np.zeros(3)

    def Place(self, X=np.zeros(3), angles=np.zeros(3)):
        self.X = X
        self.angles = angles
        transform_coord = CoordTrans.CoordTrans(X=self.X, angles=self.angles)
        transform_coord.TransfrmPoint()
        fTrCoord.TransfrmPoint(xtr,ytr,ztr);
        fTrCoord.SetPosition(xtr,ytr,ztr);

