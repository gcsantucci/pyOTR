import sys
import numpy as np
import Config as cf


class Beam():
    def __init__(self):
        self.PID = cf.beam['PID']
        self.chunck = cf.beam['chunck']
        self.Z0 = cf.beam['Z0']

    def PrepareData(self, X, V):
        assert X.shape[1] == V.shape[1] == 3
        assert X.shape[0] == V.shape[0]
        n = X.shape[0] // self.chunck
        cf.logger.info(f'Dividing the data into {n} chuncks')
        X = X[:n * self.chunck].reshape(n, self.chunck, 3)
        V = V[:n * self.chunck].reshape(n, self.chunck, 3)
        return X, V

    def GenerateRaysX(self):
        cf.logger.info(
            f'Generating {self.nrays:,} rays at random positions on a {self.size:.0f} square.')
        X = self.size * np.random.uniform(-1., 1., (self.nrays, 3))
        X[:, 2] = self.Z0
        return X

    def GenerateRaysV(self, n):
        Vtype = cf.beam['Vtype']
        if Vtype == 'parallel':
            V = np.zeros(n)
            V[:, 2] = 1.
            return V
        elif Vtype == 'divergent':
            cf.logger.info('Not yet implemented...exiting')
        else:
            cf.logger.info('Unknown velocity distribution...exiting')
        sys.exit()

    def GenerateBeam(self):
        if self.PID == 22:
            cf.logger.info(f'Selected Photon Beam')
            Xtype = cf.beam['Xtype']
            if Xtype == 'square':
                self.nrays = cf.beam['nrays']
                self.size = cf.beam['size']
                X = self.GenerateRaysX()
            elif Xtype == 'testimage':
                X = np.load('data/test_images.npy')
                X = X * 10
                X[:, 2] = self.Z0
            else:
                cf.logger.info('Unknown position distribution...exiting')
                sys.exit()
            V = self.GenerateRaysV(X.shape)
            return X, V
        elif self.PID == 2212:
            cf.logger.info(f'Selected Proton Beam')
            cf.logger.info('Not yet implemented...exiting')
        else:
            cf.logger.info(
                f'Unkown particle beam, please selected 22 for photons or 2212 for protons in the Config Module.\nExiting')
        sys.exit()
