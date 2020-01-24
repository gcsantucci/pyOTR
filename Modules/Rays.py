import numpy as np


class Rays:
    def __init__(self, X=np.array([[0., 0., -1.]]), V=np.array([[0., 0., 1.]])):
        self.X = X
        self.V = V

    def SetPosition(self, X):
        self.X = X

    def SetDirection(self, V):
        self.V = V

    def GetPosition(self):
        return self.X

    def GetDirection(self):
        return self.V
