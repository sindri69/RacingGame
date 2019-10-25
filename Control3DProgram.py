from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *


class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(0, 1, 0), Point(0, 1, 1), Vector(0, 1, 0))
        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(pi/2, 4/3, 0.3, 30)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()
        self.cube.set_vertices(self.shader)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.w_key_down = False  
        self.s_key_down = False  
        self.a_key_down = False  
        self.d_key_down = False

        self.shader.set_light_position(Point(10.0, 10.0, 10.0))
        self.shader.set_light_diffuse(0.8, 0.3, 0.4)
        self.shader.set_light_specular(0.8, 0.3, 0.4)
        self.shader.set_light_ambiance(0.1, 0.1, 0.1)

        self.white_background = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        
        self.playerMove(delta_time)

    # def ballCollision(self):
    #     ballVec = Vector(self.view_matrix.eye.x - self.ballPosX, 0.0, self.view_matrix.eye.z - self.ballPosZ)
    #     distance = ballVec.__len__()
    #     if distance < self.radius:
    #         self.sphereMatB = random.uniform(0,1)
    #         self.sphereMatG = random.uniform(0,1)
    #         self.sphereMatR = random.uniform(0,1)


    def playerMove(self, delta_time):

        if self.w_key_down: 
            self.view_matrix.slide(0, 0, -2 * delta_time)
        if self.s_key_down:
            self.view_matrix.slide(0, 0, 1 * delta_time)
        if self.a_key_down:
            self.view_matrix.pitch(-pi * delta_time)
        if self.d_key_down:
            self.view_matrix.pitch(pi * delta_time)
        

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        glViewport(0, 0, 800, 600)

        self.model_matrix.load_identity()
        #self.cube.set_vertices(self.shaderself.shader)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        # self.shader.set_light_position(Point(10.0, 10.0, 10.0))
        # self.shader.set_light_diffuse(0.8, 0.3, 0.4)
        # self.shader.set_light_specular(0.8, 0.3, 0.4)
        # self.shader.set_light_ambiance(0.1, 0.1, 0.1)

        # self.shader.set_light1_position(Point(1.0, 1.0, 1.0))
        # self.shader.set_light1_diffuse(0.3, 0.6, 0.2)
        # self.shader.set_light1_specular(0.8, 0.3, 0.4)
        # self.shader.set_light1_ambiance(0.1, 0.1, 0.1)

        # self.shader.set_light2_direction(Point(0.0, -1.0, 0.0))
        # self.shader.set_light2_diffuse(0.4, 0.8, 0.8)
        # self.shader.set_light2_specular(0.6, 0.3, 0.4)
        # self.shader.set_light2_ambiance(0.1, 0.0, 0.0)


        #floor
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.0, -0.2, 8.0)  
        self.model_matrix.add_scale(32.0, 0.4, 32.0)  
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_diffuse(0.9,0.9,0.9)
        self.shader.set_material_shininess(2)
        self.cube.set_vertices(self.shader)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()
        
        pygame.display.flip()


    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Quitting!")
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        print("Escaping!")
                        exiting = True

                    if event.key == K_w:
                        self.w_key_down = True
                    elif event.key == K_s:
                        self.s_key_down = True
                    elif event.key == K_a:
                        self.a_key_down = True
                    elif event.key == K_d:
                        self.d_key_down = True
                elif event.type == pygame.KEYUP:

                    if event.key == K_w:
                        self.w_key_down = False
                    elif event.key == K_s:
                        self.s_key_down = False
                    elif event.key == K_a:
                        self.a_key_down = False
                    elif event.key == K_d:
                        self.d_key_down = False
            
            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()
   
    
    # def drawSphere(self):
    #     self.sphere.set_vertices(self.shader)
    #     self.model_matrix.push_matrix()
    #     self.model_matrix.add_translation(self.ballPosX, 1.0, self.ballPosZ)
    #     self.shader.set_material_diffuse(self.sphereMatR, self.sphereMatG, self.sphereMatB)
    #     self.shader.set_material_specular(0.4, 0.4, 0.4)
    #     self.shader.set_model_matrix(self.model_matrix.matrix)
    #     self.sphere.draw(self.shader)
    #     self.model_matrix.pop_matrix()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()