import numpy as np
import Config as cf
import Foil
import Mirror
import ImagePlane


def Conv(deg):
    return (np.pi * deg) / 180.


def GetGeometry():

    components = []

    calib = Foil.CalibrationFoil(normal=cf.foil['normal'], diam=cf.foil['D'])
    calib.Place(X=np.zeros((1, 3)), angles=np.array([0., np.pi / 2, 0.]))
    calib.SetName('CalibFoil')

    M1 = Mirror.PlaneMirror(normal=np.array([[0., 0., -1.]]), R=50.)
    M1.Place(X=np.zeros((1, 3)),
             angles=np.array([0., Conv(45), 0.]), yrot=True)
    M1.SetName('PlaneMirror45')

    M2 = Mirror.ParaMirror()
    M2.Place(X=np.array([[1100., 0., 0.]]), angles=np.array([0., 0., 0.]))
    M2.SetName('ParaMirror')

    image = ImagePlane.ImagePlane(R=100.)
    image.Place(X=np.array([[1100., -10., 0.]]),
                angles=np.array([0., Conv(90), 0.]))
    image.SetName('ImagePlane')

    # components.append(calib)
    components.append(M1)
    components.append(M2)
    components.append(image)

    return components
