import random
import numpy as np

import Ray

#def GetRay(queue, beam, light, otr_components):
def GetRay(queue, calib):
    #foil = otr_components[0]
    #mirrors = otr_components[1]
    #camera = otr_components[-1]

    #x = 200.*random.random()
    #y = 200.*random.random()
    
    x = np.random.normal(0., 3.)
    y = np.random.normal(0., 3.)
    z = -1.
    iray = Ray.Ray(X=np.array([x, y, z]), V=np.array([0., 0., 1.]))
    calib.RayTransport(iray)
    x,   y,  z = iray.GetPosition()
    vx, vy, vz = iray.GetDirection()

    queue.put((x, y, vz))
