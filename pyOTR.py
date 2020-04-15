import concurrent.futures
import numpy as np
import sys
sys.path.append('Modules/')
import Config as cf
import Foil
import Mirror
import ImagePlane
import OpticalSystem


def Conv(deg):
    return (np.pi * deg) / 180.


@cf.timer
def PrepareData(X, V):
    assert X.shape[1] == V.shape[1] == 3
    assert X.shape[0] == V.shape[0]
    chunck = 1_000
    n = X.shape[0] // chunck
    cf.logger.info(f'Dividing the data into {n} chuncks')
    Xc = X[:n * chunck].reshape(n, chunck, 3)
    Vc = V[:n * chunck].reshape(n, chunck, 3)
    return np.array(Xc), np.array(Vc)


@cf.timer
def GenerateRays(nrays=100_000, xmax=25.):
    cf.logger.info(
        f'Generating {nrays:,} rays at random positions in a {xmax:.0f}x{xmax:.0f} square!')
    X, V = [], []
    for i in range(nrays):
        x = xmax * np.random.uniform(-1., 1., 3)
        x[-1] = -100.
        v = [0., 0., 1.]
        X.append(x)
        V.append(v)
    return np.array(X), np.array(V)


@cf.timer
def SimulateOTR():
    # nrays = cf.nrays
    # xmax = cf.xmax
    # cf.logger.info(f'Tracing {nrays:,} rays!')
    # X, V = GenerateRays(nrays=nrays, xmax=xmax)

    files = 'data/test_images.npy'
    X = np.load(f'{files}')
    X = X * 10
    X[:, 2] = -100.
    V = np.array([[0., 0., 1.]] * X.shape[0])

    np.save(f'{cf.name}_Xinitial', X)
    np.save(f'{cf.name}_Vinitial', V)
    X, V = PrepareData(X, V)

    calib = Foil.CalibrationFoil(
        normal=cf.foil['normal'], diam=cf.foil['diam'], name='CalibFoil')
    calib.Place(X=np.zeros((1, 3)), angles=np.array([0., np.pi / 2, 0.]))

    mirror1 = Mirror.PlaneMirror(normal=np.array([[0., 0., -1.]]), R=50.)
    mirror1.Place(X=np.array([[0., 0., 0.]]),
                  angles=np.array([0., Conv(45), 0.]), yrot=True)

    M2 = Mirror.ParaMirror(name='ParaMirror')
    M2.Place(X=np.array([[1100., 0., 0.]]), angles=np.array([0., 0., 0.]))

    image = ImagePlane.ImagePlane(R=100.)
    image.Place(X=np.array([[1100., -10., 0.]]),
                angles=np.array([0., Conv(90), 0.]))

    system = OpticalSystem.OpticalSystem()
    # system.AddComponent(calib)
    system.AddComponent(mirror1)
    system.AddComponent(M2)
    system.AddComponent(image)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        results = executor.map(system.TraceRay, X, V)
        for i, result in enumerate(results):
            if i % 100 == 0:
                cf.logger.debug(f'Running data chunck: {i}')
            x, v = result
            assert x.shape == v.shape
            if i == 0:
                Xf = np.array(x)
                Vf = np.array(v)
            else:
                Xf = np.concatenate((Xf, x), axis=0)
                Vf = np.concatenate((Vf, v), axis=0)

    Xf = np.array(Xf)
    Vf = np.array(Vf)

    np.save(f'{cf.name}_Xfinal', Xf)
    np.save(f'{cf.name}_Vfinal', Vf)


if __name__ == '__main__':

    cf.GetTime(start=True)

    SimulateOTR()

    cf.GetTime(start=False)
