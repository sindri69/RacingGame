from Base3DObjects import *

class Car:
    	  def __init__(self, x, y, z, angle=0.0, length=4, max_steering=30, max_acceleration=5.0):
          self.position = Vector(x, y, z)
          self.velocity = Vector(0.0, 0.0, 0.0)
          self.angle = angle
          self.length = length
          self.max_acceleration = max_acceleration
          self.max_steering = max_steering
          self.acceleration = 0.0
          self.steering = 0.0
          self.brake_deceleration = 0.0

        def update(self, delta_time):
          self.velocity += (self.acceleration * delta_time, 0)
          turning_radius = self.length / sin(self.steering)
          angular_velocity = self.velocity.x / turning_radius

          if self.steering:
        	  turning_radius = self.length / sin(self.steering)
            angular_velocity = self.velocity.x / turning_radius
          else: 
            angular_velocity = 0

          self.position += self.velocity.rotate(-self.angle) * delta_time
          self.angle += degrees(angular_velocity) * delta_time

