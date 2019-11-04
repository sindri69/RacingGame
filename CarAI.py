from Base3DObjects import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *

class CarAI:
    def __init__(self, tStart, tEnd, p):
        self.p = p
        self.carPosition = p[0]
        self.carHeading = atan2(p[0].x, p[0].z)
        self.tStart = tStart
        self.tEnd = tEnd

    def update(self, totalTime):
        if self.tStart < totalTime and totalTime < self.tEnd:
            t = (totalTime - self.tStart) / (self.tEnd - self.tStart)
            pX = pow((1-t), 3) * self.p[0].x + 3 * t * pow((1-t), 2) * self.p[1].x + 3 * pow(t, 2) * (1 - t) * self.p[2].x + pow(t, 3) * self.p[3].x
            pZ = pow((1-t), 3) * self.p[0].z + 3 * t * pow((1-t), 2) * self.p[1].z + 3 * pow(t, 2) * (1 - t) * self.p[2].z + pow(t, 3) * self.p[3].z
            pY = self.p[0].y
            self.carPosition = Vector(pX, pY, pZ)
            u = pow((1-t), 2) * (self.p[1].x - self.p[0].x) + 2 * t * (1-t) * (self.p[2].x - self.p[1].x) + pow(t, 2) * (self.p[3].x - self.p[2].x)
            v = pow((1-t), 2) * (self.p[1].z - self.p[0].z) + 2 * t * (1-t) * (self.p[2].z - self.p[1].z) + pow(t, 2) * (self.p[3].z - self.p[2].z)
            self.carHeading = atan2(u, v)