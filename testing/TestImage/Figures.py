import numpy as np

class Rectangle:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def Pass(self, x, y):
        if self.x1 < x < self.x2 and self.y1 < y < self.y2:
            return True
        return False

class RotatedRectangle(Rectangle):
    def __init__(self, x1, x2, y1, y2, alpha=45., x0=1., y0=1.):
        Rectangle.__init__(self, x1, x2, y1, y2)
        self.alpha = (alpha * np.pi) / 180.
        self.x0 = x0 + np.cos(self.alpha)
        self.y0 = y0 + np.sin(self.alpha)

    def Pass(self, x, y):
        x, y = x - self.x0, y - self.y0
        xp = np.cos(self.alpha)*x + np.sin(self.alpha)*y
        yp = np.sin(self.alpha)*x - np.cos(self.alpha)*y
        yp = yp + (self.y2 - self.y1)/2
        return Rectangle.Pass(self, xp, yp)

class Circle:
    def __init__(self, x0, y0, R):
        self.x0 = x0
        self.y0 = y0
        self.R = R

    def Pass(self, x, y):
        if (x - self.x0)**2 + (y - self.y0)**2 < self.R**2:
            return True
        return False
