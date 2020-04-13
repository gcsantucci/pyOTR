import numpy as np


class OpticalSystem():
    def __init__(self):
        print('Hello from OpticalSystem')
        self.components = []

    def AddComponent(self, component):
        self.components.append(component)

    def TraceRay(self, X, V):
        if len(self.components) == 0:
            print('ERROR! No optical components were declared.\nExiting...')
            return 0, 0
        for comp in self.components:
            X, V = comp.RaysTransport(X, V)
        return X, V
