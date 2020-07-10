import numpy as np
import Config as cf


class Beam():
    def __init__(self):
        self.nrays = cf.beam['nrays']
        self.chunck = cf.beam['chunck']
        self.x = cf.beam['x']
        self.y = cf.beam['y']
        self.z = cf.beam['z']
        self.cov = cf.beam['cov']
        
    def PrepareData(self, X, V):
        assert X.shape[1] == V.shape[1] == 3
        assert X.shape[0] == V.shape[0]
        n = X.shape[0] // self.chunck
        cf.logger.info(f'Dividing the data into {n:,} pieces')
        X = X[:n * self.chunck].reshape(n, self.chunck, 3)
        V = V[:n * self.chunck].reshape(n, self.chunck, 3)
        return X, V

    def GenerateRaysV(self, n):
        Vtype = cf.beam['Vtype']
        if Vtype == 'parallel':
            V = np.zeros(n)
            V[:, 2] = 1.
            return V
        elif Vtype == 'divergent':
            vx = 0.05 * np.random.uniform(0., 1.)
            vy = 0.05 * np.random.uniform(0., 1.)
            vz = np.sqrt(1 - vx*vx - vy*vy)            
            V = np.random.multivariate_normal(mean, self.cov, n)
            cf.logger.info('Not yet implemented...exiting')
        else:
            cf.logger.info('Unknown velocity distribution...exiting')
        sys.exit()

    def GenerateBeam(self):
        cf.logger.info(f'Selected Proton Beam')
        mean = [self.x, self.y, self.z]
        X = np.random.multivariate_normal(mean, self.cov, self.nrays)
        V = self.GenerateRaysV(X.shape)
        return X, V
