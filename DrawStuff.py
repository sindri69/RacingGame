from Shaders import *
from Matrices import *
from Car import *

def drawCar1(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_translation(control.carSimple1.position.x, control.carSimple1.position.y, control.carSimple1.position.z)
    control.model_matrix.add_rotateY(control.carSimple1.carHeading)
    control.model_matrix.add_scale(2.0, 1.5, 4.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.shader.set_material_diffuse(Color(0.2,0.8,0.4))
    control.shader.set_material_shininess(2)
    control.cube.set_vertices(control.shader)
    control.cube.draw(control.shader)
    control.model_matrix.pop_matrix()

def drawCar2(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_translation(control.carSimple2.position.x, control.carSimple2.position.y, control.carSimple2.position.z)
    control.model_matrix.add_rotateY(control.carSimple2.carHeading)
    control.model_matrix.add_scale(2.0, 1.5, 4.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.shader.set_material_diffuse(Color(0.2,0.8,0.4))
    control.shader.set_material_shininess(2)
    control.cube.set_vertices(control.shader)
    control.cube.draw(control.shader)
    control.model_matrix.pop_matrix()

def drawCarAI(control):
    print(control.carAI.carPosition.x, control.carAI.carPosition.y, control.carAI.carPosition.z)
    control.model_matrix.push_matrix()
    control.model_matrix.add_translation(control.carAI.carPosition.x, control.carAI.carPosition.y, control.carAI.carPosition.z)
    control.model_matrix.add_rotateY(control.carAI.carHeading)
    control.model_matrix.add_scale(2.0, 1.5, 4.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.shader.set_material_diffuse(Color(0.2,0.8,0.4))
    control.shader.set_material_shininess(2)
    control.cube.set_vertices(control.shader)
    control.cube.draw(control.shader)
    control.model_matrix.pop_matrix()

def drawTree(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_translation(3.0, 1.0, 3.0)
    control.model_matrix.add_scale(2.0, 1.5, 4.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.tree.draw(control.shader)
    control.model_matrix.pop_matrix()

def drawGrass(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_scale(3.0, 0.4, 3.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.grass.draw(control.shader)
    control.model_matrix.pop_matrix()


def drawtest(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_scale(0.5, 0.5, 0.5)
    control.model_matrix.add_translation(10, 1.0, 1.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.test.draw(control.shader)
    control.model_matrix.pop_matrix() 

def drawLambo(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_scale(2.0, 2.0, 2.0)
    control.model_matrix.add_translation(2, 1.0, 3.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.lambo.draw(control.shader)
    control.model_matrix.pop_matrix()    

def drawForrest(control, howmanytrees):
    for x in range (1, howmanytrees):
        control.model_matrix.push_matrix()
        control.model_matrix.add_translation(1.0 * x, 1.0, 1.0 * x)
        control.model_matrix.add_scale(2.0, 1.5, 4.0)
        control.shader.set_model_matrix(control.model_matrix.matrix)
        control.tree.draw(control.shader)
        control.model_matrix.pop_matrix()

def drawfloor(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_translation(20.0, -0.2, 20.0)
    control.model_matrix.add_scale(80.0, 0.4, 80.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.shader.set_material_diffuse(Color(0.9,0.9,0.9))
    control.shader.set_material_shininess(2)
    control.cube.set_vertices(control.shader)
    control.cube.draw(control.shader)
    control.model_matrix.pop_matrix()

def drawTrack(control, racetrack):
    control.model_matrix.push_matrix()
    control.model_matrix.add_translation(0.0, -0.2, 0.0)
    # control.model_matrix.add_scale(40.0, 0.2, 40.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.shader.set_material_diffuse(Color(0.9,0.9,0.9))
    control.shader.set_material_shininess(2)
    racetrack.draw(control.shader)
    control.model_matrix.pop_matrix()