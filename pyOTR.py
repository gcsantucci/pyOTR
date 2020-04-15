import concurrent.futures
import numpy as np
import sys
sys.path.append('Modules/')
import Config as cf
import Beam
import Foil
import Mirror
import ImagePlane
import OpticalSystem


def Conv(deg):
    return (np.pi * deg) / 180.


@cf.timer
def SimulateOTR(X, V):

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

    cf.GetTime()

    beam = Beam.Beam()
    X, V = beam.GenerateBeam()
    print(X.shape)
    print(V.shape)

    SimulateOTR(X, V)

    cf.GetTime(start=False)
