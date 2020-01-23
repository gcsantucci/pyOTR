import concurrent.futures
import time
import numpy as np
import sys
# Add the directory with OTR Modules to path:                             
sys.path.append('Modules/')
sys.path.append('include/')
import Rays
import Foil


def PrepareData(X, V):
    assert X.shape[1] == V.shape[1] == 3
    assert X.shape[0] == V.shape[0]
    chunck = 1_000
    n = X.shape[0] // chunck
    r = X.shape[0] % chunck
    Xf, Vf = [], []
    for i in range(n):
        Xf.append(X[chunck * i:chunck * (i + 1)])
        Vf.append(V[chunck * i:chunck * (i + 1)])
    if r > 0:
        Xf.append(X[chunck * n:])
        Vf.append(V[chunck * n:])
    return np.array(Xf), np.array(Vf)

def GenerateRays(nrays=100_000, xmax=25.):
    X, V = [], []
    for i in range(nrays):
        x = xmax * np.random.uniform(-1., 1., 3)
        x[-1] = -1.
        v = [0., 0., 1.]
        X.append(x)
        V.append(v)
    return np.array(X), np.array(V)

def main():
    nrays = 100_000
    xmax = 25.
    t0 = time.time()
    X, V = GenerateRays(nrays=nrays, xmax=xmax)
    rays = Rays.Rays(X=X, V=V)
    print(f'Time to generate {nrays:,} rays: {round(time.time() - t0, 2)} s')
    X, V = PrepareData(X, V)
    calib = Foil.CalibrationFoil(normal=np.array([[0, 1, 0]]), diam=50.)

    t0 = time.time()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(calib.RaysTransport, X, V)
        for i, result in enumerate(results):
            if i % 100 == 0:
                print(i)
            x, v = result
            if i == 0:
                Xf = np.array(x)
                Vf = np.array(v)
            else:
                Xf = np.concatenate((Xf, x), axis=1)
                Vf = np.concatenate((Vf, v), axis=1)

    Xf = np.array(Xf)
    Vf = np.array(Vf)
    print(f'Time to transport {nrays:,} rays: {time.time() - t0:.2f} s')
    
    np.save('output/Xfinal', Xf)
    np.save('output/Vfinal', Vf)

if __name__ == '__main__':
    main()
