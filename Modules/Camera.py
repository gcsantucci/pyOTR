class Camera:
      def __init__(self, npxlX=484, npxlY=704, fdist=60.):
          self.npxlX = npxlX
          self.npxlY = npxlY
          self.fdist = fdist

      def __del__(self):
          print('Camera deleted.')

      def SetPixels(self, npxlX, npxlY):
          self.npxlX = npxlX
          self.npxlY = npxlY
      
      def SetDistance(self, dist):
            self.fdist = dist
          
      def GetPixels(self):
          return self.npxlX, self.npxlY

      def GetDistance(self):
            return self.fdist
