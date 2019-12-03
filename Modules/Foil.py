import numpy as np
import CoordTrans

foils = {
      0: 'Blank',
      1: 'Fluorescent',
      2: 'Calibration',
      3: 'Ti1',
      4: 'Ti2',
      5: 'Ti3',
      6: 'Ti4',
      7: 'Cross'
      }

#Generic Foil class, common among all Foils:
class Foil:
      def __init__(self, ID=1, normal=np.array([0,1,0]), diam=55., epsilon_dia=0):
          self.ID = ID
          self.epsilon_dia = epsilon_dia
          self.fFdmtr = diam
          self.normal = normal

      def __del__(self): print('Foil deleted.') 
      def GetID(self): return self.ID
      def GetType(self): return foils[self.ID]
      def GetDiameter(self): return self.fFdmtr

      def PlaneIntersect(self, pos, V):
          pos_int = []
          if pos[1] == 0. or  np.abs(V[1]) <= 10e-9: return False, 0
          if pos[1]/np.abs(pos[1]) == V[1]/np.abs(V[1]): return False, 0
          t = -1.*pos[1] / V[1] #by construction! interact at y = 0
          pos_int = pos + V*t
          assert pos_int[1] < 10e-9
          if np.dot(pos_int, pos_int) >= (self.fFdmtr**2) / 4.: return False, 0
          return True, pos_int
      
      def PlaneReflect(self, V):
          return V - 2*np.dot(V, self.normal) * self.normal
      
      def PlaneTransport(self, pos, V):
          intersect, pos_int = self.PlaneIntersect(pos, V)
          if not intersect: return False, 0, 0
          return True, pos_int, self.PlaneReflect(V)

#Calibration Foil class, inherits from Generic Foil class:
#class CalibrationFoil(OpticalComponent, Foil):
class CalibrationFoil(Foil):
      def __init__(self, hole_dist=7., hole_diam=1.2,
                   normal=np.array([0.,1.,0.]), diam=55., epsilon_dia=0):
          #OpticalComponent.__init__(self)
          Foil.__init__(self, ID=2, normal=normal, diam=diam, epsilon_dia=epsilon_dia)
          self.fName = self.GetType();
          self.fHdist = hole_dist
          self.fHdmtr = hole_diam
          self.holes = self.MakeHoles()

      def MakeHoles(self):
          import os, sys, pickle
          sys.path.append('macros')
          from MakeCalibHoles import MakeHoles
          calib_pickle = 'data/calib_holes.p'
          if os.path.isfile(calib_pickle): return pickle.load(open(calib_pickle, 'rb'))
          else: return MakeHoles()
      
      def PrintHolePos(self, screen=False):
          print('Using Calibration Holes:')
          for i, ihole in enumerate(self.holes):
              print('{0} {1} {2}'.format(i, ihole[0], ihole[2]))

      def PassHole(self, pos):
          for i, ihole in enumerate(self.holes):
              val = np.dot(ihole[:-1] - pos, ihole[:-1] - pos)
              if val <= np.dot(ihole[-1], ihole[-1]) / 4.: return True
          return False #not passing through a hole

      def RayTransport(self, ray):
          #Transform into the local foil coordinates   
          #Foil.Place(0.,CONVERT(90)+CONVERT(BMANGL),CONVERT(45), 0.,0.,0.);
          #fTrCoord = CoordTrans.CoordTrans(X=np.zeros(3),angles=np.array([0., np.radians(90), np.radians(45)]))
          #foil_global = np.array([-5., 3., 2.])
          euler = np.array([0., np.pi/2, 0.]) 
          #fTrCoord = CoordTrans.CoordTrans(X=foil_global, angles=euler)            
          fTrCoord = CoordTrans.CoordTrans(X=np.zeros(3), angles=euler)
          pos = ray.GetPosition()
          pos = fTrCoord.TransfrmPoint(pos)
          V = ray.GetDirection()
          V = fTrCoord.TransfrmVec(V)

          transport, pos_int, V_reflected = self.PlaneTransport(pos, V)
          if not transport: return 0 #no intersection with the Foil
          if self.PassHole(pos_int): V_reflected = V #ray passed through hole, so no reflection

          #Transform back to the global coordinate system
          pos_int = fTrCoord.TransfrmPoint(pos_int, inv=True)
          V_reflected = fTrCoord.TransfrmVec(V_reflected, inv=True)
          ray.SetPosition(pos_int)
          ray.SetDirection(V_reflected)
