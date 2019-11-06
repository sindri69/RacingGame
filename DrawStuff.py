from Shaders import *
from Matrices import *
from math import *

def drawCar1(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_translation(control.carSimple1.position.x, control.carSimple1.position.y, control.carSimple1.position.z)
    control.model_matrix.add_rotateY(control.carSimple1.carHeading + pi/2)
    control.model_matrix.add_scale(0.60, 0.60, 0.60)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.shader.set_material_diffuse(Color(0.2,0.8,0.4))
    control.shader.set_material_shininess(2)
    control.car_model.draw(control.shader)
    control.model_matrix.pop_matrix()

def drawCar2(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_translation(control.carSimple2.position.x, control.carSimple2.position.y, control.carSimple2.position.z)
    control.model_matrix.add_rotateY(control.carSimple2.carHeading + pi/2)
    control.model_matrix.add_scale(0.6, 0.6, 0.6)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.car_model2.draw(control.shader)
    control.model_matrix.pop_matrix()

def drawCarAI(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_translation(control.carAI.carPosition.x, control.carAI.carPosition.y, control.carAI.carPosition.z)
    control.model_matrix.add_rotateY(control.carAI.carHeading + pi/2)
    control.model_matrix.add_scale(0.6, 0.6, 0.6)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.car_model3.draw(control.shader)
    control.model_matrix.pop_matrix()

def drawTree(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_translation(3.0, 1.0, 3.0)
    control.model_matrix.add_scale(2.0, 1.5, 4.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.tree.draw(control.shader)
    control.model_matrix.pop_matrix()

def drawGrass(control, carsimple):
    control.skysphere_shader.use()
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, control.texture_id_grass)                 
    control.skysphere_shader.set_diffuse_tex(0)
    control.textureCube.set_uv(control.skysphere_shader)
    for i in range(-10, 10):
        for j in range(-10, 10):
                
                control.model_matrix.push_matrix()
                control.model_matrix.add_translation(i*12.0 + 12*floor(carsimple.position.x /12.0), -0.2, j*12.0 + 12*floor(carsimple.position.z/12.0))
                control.model_matrix.add_scale(12.0, 0.4, 12.0)
                control.skysphere_shader.set_model_matrix(control.model_matrix.matrix)
                control.textureCube.draw()
                control.model_matrix.pop_matrix()
    control.shader.use()

def drawGates(control):
    for gate in control.track.gateArr:
        control.model_matrix.push_matrix()
        control.model_matrix.add_translation(gate[0].x,gate[0].y, gate[0].z)
        # control.model_matrix.add_rotateZ(pi)
        control.model_matrix.add_scale(5.0, 3.0, 5.0)
        control.model_matrix.add_rotateX(pi)
        control.model_matrix.add_rotateY(gate[1] - pi/2)
        control.shader.set_model_matrix(control.model_matrix.matrix)
        control.gate.draw(control.shader)
        control.model_matrix.pop_matrix() 

def drawLambo(control):
    control.model_matrix.push_matrix()
    control.model_matrix.add_scale(2.0, 2.0, 2.0)
    control.model_matrix.add_translation(2, 1.0, 3.0)
    control.shader.set_model_matrix(control.model_matrix.matrix)
    control.lambo.draw(control.shader)
    control.model_matrix.pop_matrix()    

def drawForrest(control):
    for tree in control.track.treeArr:
        control.model_matrix.push_matrix()
        control.model_matrix.add_translation(tree.x, tree.y - 0.2, tree.z)
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