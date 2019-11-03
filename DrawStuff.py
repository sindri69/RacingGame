from Shaders import *
from Matrices import *
from Car import *

def drawCar1(car1):
    car1.model_matrix.push_matrix()
    car1.model_matrix.add_translation(car1.carSimple1.position.x, car1.carSimple1.position.y, car1.carSimple1.position.z)
    car1.model_matrix.add_rotateY(car1.carSimple1.carHeading)
    car1.model_matrix.add_scale(2.0, 1.5, 4.0)
    car1.shader.set_model_matrix(car1.model_matrix.matrix)
    car1.shader.set_material_diffuse(Color(0.2,0.8,0.4))
    car1.shader.set_material_shininess(2)
    car1.cube.set_vertices(car1.shader)
    car1.cube.draw(car1.shader)
    car1.model_matrix.pop_matrix()

def drawCar2(car2):
    car2.model_matrix.push_matrix()
    car2.model_matrix.add_translation(car2.carSimple2.position.x, car2.carSimple2.position.y, car2.carSimple2.position.z)
    car2.model_matrix.add_rotateY(car2.carSimple2.carHeading)
    car2.model_matrix.add_scale(2.0, 1.5, 4.0)
    car2.shader.set_model_matrix(car2.model_matrix.matrix)
    car2.shader.set_material_diffuse(Color(0.2,0.8,0.4))
    car2.shader.set_material_shininess(2)
    car2.cube.set_vertices(car2.shader)
    car2.cube.draw(car2.shader)
    car2.model_matrix.pop_matrix()

def drawTree(self):
    self.model_matrix.push_matrix()
    self.model_matrix.add_translation(3.0, 1.0, 3.0)
    self.model_matrix.add_scale(2.0, 1.5, 4.0)
    self.shader.set_model_matrix(self.model_matrix.matrix)
    self.tree.draw(self.shader)
    self.model_matrix.pop_matrix()

def drawGrass(self):
    self.model_matrix.push_matrix()
    self.model_matrix.add_scale(3.0, 0.4, 3.0)
    self.shader.set_model_matrix(self.model_matrix.matrix)
    self.grass.draw(self.shader)
    self.model_matrix.pop_matrix()


def drawtest(self):
    self.model_matrix.push_matrix()
    self.model_matrix.add_scale(0.5, 0.5, 0.5)
    self.model_matrix.add_translation(10, 1.0, 1.0)
    self.shader.set_model_matrix(self.model_matrix.matrix)
    self.test.draw(self.shader)
    self.model_matrix.pop_matrix() 

def drawLambo(self):
    self.model_matrix.push_matrix()
    self.model_matrix.add_scale(2.0, 2.0, 2.0)
    self.model_matrix.add_translation(2, 1.0, 3.0)
    self.shader.set_model_matrix(self.model_matrix.matrix)
    self.lambo.draw(self.shader)
    self.model_matrix.pop_matrix()    

def drawForrest(self, howmanytrees):
    for x in range (1, howmanytrees):
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(1.0 * x, 1.0, 1.0 * x)
        self.model_matrix.add_scale(2.0, 1.5, 4.0)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.tree.draw(self.shader)
        self.model_matrix.pop_matrix()

def drawfloor(self):
    self.model_matrix.push_matrix()
    self.model_matrix.add_translation(20.0, -0.2, 20.0)
    self.model_matrix.add_scale(80.0, 0.4, 80.0)
    self.shader.set_model_matrix(self.model_matrix.matrix)
    self.shader.set_material_diffuse(Color(0.9,0.9,0.9))
    self.shader.set_material_shininess(2)
    self.cube.set_vertices(self.shader)
    self.cube.draw(self.shader)
    self.model_matrix.pop_matrix()
