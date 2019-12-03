class Mirror:
      def __init__(self, x=1., y=1., fdist=2.):
          self.x = x
          self.y = y
          self.fdist = fdist

      def __del__(self):
          print('Mirror deleted.')

      def SetPosition(self, x, y):
          self.x = x
          self.y = y
      
      def SetFocalDistance(self, dist):
            self.fdist = dist

      def SetReflectance(self, reflectance):
            self.reflectance = reflectance
          
      def GetPosition(self):
          return self.x, self.y

      def GetDistance(self):
            return self.fdist
