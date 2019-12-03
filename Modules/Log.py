import os
class LogFile:
      def __init__(self, logfile):
          self.VERBOSE = logfile
          if(logfile): self.log = open(logfile, 'w')
          else: self.log = None

      def __del__(self):
          self.log.close()

      def Log(self, message, screen=False):
          if self.VERBOSE: self.log.write(message + '\n')
          if screen: print(message)
