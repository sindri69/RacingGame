from Base3DObjects import *

class CarPhysics:
    def __init__(self):
        self.airResist = 0.4257 #magic
        self.groundResist = 12.8 #magic
        self.engine = 0.0
        self.velocity = Vector(0.0, 0.0, 0.1)
        self.mass = 1000.0 #change
        self.position = Vector(1.0, 1.0, 1.0)
    def update(self, delta_time):
        unit = self.velocity
        unit.normalize
        traction = unit * self.engine
        aerodrag = self.velocity * (-self.airResist) * self.velocity.__len__()
        rollingResist =  self.velocity * (-self.groundResist) 
        force = traction + aerodrag + rollingResist
        accel = force / self.mass
        self.velocity += accel *  delta_time
        self.position += self.velocity * delta_time 
class Wheel:
    def __init__(self, position, radius):
        self.position = position
        self.wheelSpeed = 0.0
        self.wheelRadius = radius
        self.wheelInertia = radius * radius

