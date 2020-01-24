import concurrent.futures
import numpy as np
import sys
sys.path.append('Modules/')
import Config as cf
import Rays
import Foil


@cf.timer
def PrepareData(X, V):
    assert X.shape[1] == V.shape[1] == 3
    assert X.shape[0] == V.shape[0]
    chunck = 1_000
    n = X.shape[0] // chunck
    r = X.shape[0] % chunck
    cf.logger.info(f'Dividing the data into {n+1} chuncks')

    Xc, Vc = [], []
    for i in range(n):
        Xc.append(X[chunck * i: chunck * (i + 1)])
        Vc.append(V[chunck * i: chunck * (i + 1)])
    if r > 0:
        Xc.append(X[chunck * n:])
        Vc.append(V[chunck * n:])
    return np.array(Xc), np.array(Vc)


@cf.timer
def GenerateRays(nrays=100_000, xmax=25.):
    cf.logger.info(
        f'Generating {nrays:,} rays at random positions in a {xmax:.0f}x{xmax:.0f} square!')
    X, V = [], []
    for i in range(nrays):
        x = xmax * np.random.uniform(-1., 1., 3)
        x[-1] = -1.
        v = [0., 0., 1.]
        X.append(x)
        V.append(v)
    return np.array(X), np.array(V)


@cf.timer
def TransportRays():
    nrays = cf.nrays
    xmax = cf.xmax
    cf.logger.info(f'Tracing {nrays:,} rays!')

    X, V = GenerateRays(nrays=nrays, xmax=xmax)
    np.save(f'{cf.name}_Xinitial', X)
    np.save(f'{cf.name}_Vinitial', V)
    rays = Rays.Rays(X=X, V=V)
    X, V = PrepareData(X, V)
    calib = Foil.CalibrationFoil(normal=np.array([[0, 1, 0]]), diam=50.)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(calib.RaysTransport, X, V)
        for i, result in enumerate(results):
            if i % 100 == 0:
                cf.logger.debug(f'Running data chunck: {i}')
            x, v = result
            if i == 0:
                Xf = np.array(x)
                Vf = np.array(v)
            else:
                Xf = np.concatenate((Xf, x), axis=1)
                Vf = np.concatenate((Vf, v), axis=1)

    Xf = np.array(Xf)
    Vf = np.array(Vf)

    np.save(f'{cf.name}_Xfinal', Xf)
    np.save(f'{cf.name}_Vfinal', Vf)


if __name__ == '__main__':

    TransportRays()

    cf.GetTime(False)
