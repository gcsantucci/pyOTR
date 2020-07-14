import numpy as np
from numpy import cos, sin, pi


def RotateZ(ray, angle):
    M = np.array([[cos(angle), -sin(angle), 0.],
                  [sin(angle), cos(angle), 0.],
                  [0., 0., 1.]
                  ])
    return M.dot(ray)


def RotateX(ray, angle):
    M = np.array([[1., 0., 0.],
                  [0., cos(angle), -sin(angle)],
                  [0., sin(angle), cos(angle)]
                  ])
    return M.dot(ray)


def Landau(mu, sigma):
    x = (x - mu) / sigma
    A = 1 / (2 * pi)
    A * np.exp(-(x + np.exp(-x)) / 2)


class LightDist():
    def __init__(self, seed=0):
        self.beam_gamma = 32.
        self.theta_range = 0.3  # rad

    def OtrCDF(self, x=[], pars=[]):
        y = x[0] * x[0] * pars[0] * pars[0]
        return 0.5 * ((y + 1) * np.log(y + 1) - y) / (y + 1)

    def SetScatterOption(self, h, s, o):
        # Note that hav_on negates scat_on/otr_on
        # Having scat_on/otr_on as separatue values allows user to look at
        # 1)Perfect otr -- just otr_on
        # 2)Scatter sans otr -- just scat_on
        # 3)The full combination -- otr_on/scat_on
        # 4)Perfect reflection -- all options set to false
        self.hav_on = h
        self.scat_on = s
        self.otr_on = o

    def GetScatterOption(self, type):
        if type == 1:
            return self.hav_on
        elif type == 2:
            return self.scat_on
        elif type == 3:
            return self.otr_on
        return -1

    def ScatterAngle(self, i):
        # mean / sigma are hardcoded as the values obtained for landau distributions
        # at 600 nm, averaged paralell and perpendicular striations
        # order for possible choices = {Ti - 15V - 3Cr - 3Sn - 3Al, Ti - 6Al - 4V}
        mean = [5.794, 1.986]
        sigma = [3.766, 2.663]
        angle = -1
        while(angle < 0):
            angle = 1  # -> Landau(mean[i], sigma[i])
        return angle * pi / 180.

    def SetAxesToZVelocity(self, light_ray):
        # This function rotates a vector with the coordinates of the light ray up onto the z axis
        # Once rotated, using probabilistic scatter distribution to alter direction of light ray is simple
        # Note that rotations in reverse happen in the opposite order in GetLightRay
        return_ray = light_ray.copy()
        theta, phi = self.GetAngles(return_ray)
        # need to define these rotations:
        return_ray = RotateZ(return_ray, pi / 2 - phi)
        return_ray = RotateX(return_ray, theta)
        return return_ray

    def DistributeLight(self, light_ray, sangle):
        # This is where the random scatter occurs -- sangle from scatter distribution
        # or otr distribution later in the code, then rangle randomly selected 0 - 2pi
        return_ray = np.zeros(3)
        rangle = 2 * pi * np.random.uniform(0, 1)
        return_ray[0] = light_ray[2] * sin(sangle) * cos(rangle)
        return_ray[1] = light_ray[2] * sin(sangle) * sin(rangle)
        return_ray[2] = light_ray[2] * cos(sangle)
        return return_ray

    def SetGamma(self, gamma):
        self.beam_gamma = gamma
        fOtrCdf -> SetParameter(0, fBeamGamma)
        fTht_max = fOtrCdf -> GetMaximum(0.0, fTht_range)

    def SampleOtr(self, gamma, fillh):
        if gamma != self.beam_gamma:
            self.SetGamma(gamma)
        fval = self.fTht_max * np.random.uniform(0, 1.)
        xval = fOtrCdf -> GetX(fval, 0, fTht_range)
        if fillh:
            if fHdist:
                fHdist -> Fill(xval)
            else:
                fHdist = new TH1D("ang_dist", "ang_dist", 100, 0.0, fTht_range)
                fHdist -> Fill(xval)
        return xval

    def SampleDiff(self, tht_range, fillh):
        if(tht_range == 0)
            return 0.0
        cosa = 1 + (cos(tht_range) - 1) * np.random.uniform(0, 1.)
        xval = np.arccos(cosa)
        if fillh:
            if fHdist:
                fHdist -> Fill(xval)
        else:
            fHdist = new TH1D("ang_dist", "ang_dist", 100, 0.0, fTht_range)
            fHdist -> Fill(xval)
    return xval

    def GetAngles(self, ray):
        r = np.sqrt(ray[0] * ray[0] + ray[1] * ray[1] + ray[2] * ray[2])
        return np.arccos(ray[2] / r), np.arctan2(ray[1] / ray[0])

    def GetLightRay(self, V, angl_sprd, gamma, tht_range):
        # New method
        light_ray = np.array(V)
        sangle = self.ScatterAngle(0)
        oangle
        theta_one, phi_one = self.GetAngles(light_ray)
        # Original method
        tht0, phi0 = self.GetAngles(V)
        count = 0
        rval = 1.
        # New method for OTR light distribution
        if(self.hav_on == 0):
            # Rotate axes s.t. z axis points in the direction in which particle travels
            light_ray = self.SetAxesToZVelocity(light_ray, true)
            # Choose value for oangle
            if(gamma != 0.):  # Otr light
                oangle = self.SampleOtr(gamma)
            else:
                oangle = self.SampleDiff(tht_range)
            # Incorporate scatter
            if(self.scat_on == 1):
                # Light is scattered about reflection axis given experimental data
                light_ray = self.DistributeLight(light_ray, sangle, true)
                theta_two, phi_two = self.GetAngles(light_ray)
                # Rotate into coordinate system of scattered particle
                light_ray = self.SetAxesToZVelocity(light_ray, true)
                # Light comes out in a cone with angular distribution given by OTR_CDF / SamleDiff
                if(self.otr_on == 1):
                    light_ray = self.DistributeLight(light_ray, oangle, true)
                # Rotate back - - inverse rotations have inverse order
                if(self.scat_on == 1):
                    light_ray.RotateX(-theta_two)
                    light_ray.RotateZ(-M_PI / 2 + phi_two)

                light_ray.RotateX(-theta_one)
                light_ray.RotateZ(-M_PI / 2 + phi_one)
                # Set final vx, vy, vz
                vx = light_ray[0]
                vy = light_ray[1]
                vz = light_ray[2]
        else:
            # Original method for OTR light distribution
            if(gamma != 0.):  # Otr light
                oangle = self.SampleOtr(gamma)
            else:
                oangle = self.SampleDiff(tht_range)
            count = 0
            rval = 1.
            while (rval > angl_sprd):
                if(count > 10000):
                    print("WARNING: ")
                    break
                tht1 pi / 3 * np.random.uniform(0, 1.) + tht0 - pi / 6
                phi1 = 2 * pi i * np.random.uniform(0, 1.)
                rval = self.DistanceDiff(oangle, phi0, tht0, phi1, tht1)
                count += 1
            # Calculate the ray direction
            vx = cos(phi1) * sin(tht1)
            vy = sin(phi1) * sin(tht1)
            vz = cos(tht1)
        V = np.array([vx, vy, vz])
        return V

    def DistanceDiff(self, oangle, phi0, theta0, phi1, theta1):
        lat0 = pi / 2 - theta0
        lat1 = pi / 2 - theta1
        dlat = lat1 - lat0
        dphi = phi1 - phi0
        sindl = sin(dlat / 2)
        sindphi = sin(dphi / 2)
        sina = sin(oangle / 2)
        lhs = sina * sina
        rhs = sindl * sindl + cos(lat0) * cos(lat1) * sindphi * sindphi
        return np.fabs(lhs - rhs)
