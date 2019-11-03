from Base3DObjects import *
from math import *

class CarSimple:
    def __init__(self, position):
        self.position = position
        self.carHeading = 0.0
        self.carSpeed = 0.0
        self.steerAngle = 0.0
        self.maxSteerAngle = 0.4
        self.wheelBase = 2.0
        self.maxSpeed = 40
        self.maxBackSpeed = -20
    def update(self, delta_time):
        frontWheel = self.position + Vector( sin(self.carHeading) , 0.0, cos(self.carHeading) ) * self.wheelBase/2 
        backWheel = self.position - Vector( sin(self.carHeading) , 0.0, cos(self.carHeading) ) * self.wheelBase/2  
        backWheel += Vector(sin(self.carHeading), 0.0, cos(self.carHeading)) * self.carSpeed * delta_time
        frontWheel += Vector(sin(self.carHeading + self.steerAngle), 0.0, cos(self.carHeading + self.steerAngle)) * self.carSpeed * delta_time
        self.position = (frontWheel + backWheel) / 2
        self.carHeading = atan2(frontWheel.x - backWheel.x, frontWheel.z - backWheel.z)