from OpenGL.GL import *
from OpenGL.GLU import *
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Maze import * 
from Shaders import *
from Matrices import *
from BallLogic import * 

class GraphicsProgram3D:
    def __init__(self):

        pygame.init() 
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix_mini = ViewMatrix()
        self.view_matrix.look(Point(0, 1, 0), Point(0, 1, 1), Vector(0, 1, 0))
        self.projection_matrix = ProjectionMatrix()
        #self.projection_matrix.set_orthographic(-2, 2, -2, 2, 0.5, 10)
        self.projection_matrix.set_perspective(pi/2, 4/3, 0.3, 30)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.cube = Cube()
        self.cube.set_vertices(self.shader)

        self.sphere = Sphere(25, 50)
        self.radius = 1.4
        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        self.w_key_down = False  
        self.s_key_down = False  
        self.a_key_down = False  
        self.d_key_down = False
        

        self.white_background = False
        self.size = 6
        self.maze = Maze(self.size)
        self.ballGridX = 2
        self.ballGridZ = 2
        self.ballPosX = 6.0
        self.ballPosZ = 6.0
        self.ballOri = "north"
        self.speed = 5.0
        self.ballElapsed = 0.0

        self.sphereMatR = 0.3
        self.sphereMatG = 0.3
        self.sphereMatB = 0.3
    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.ballElapsed -= delta_time
        self.angle += pi * delta_time
        if self.angle > 2 * pi:
            self.angle -= (2 * pi)
        if self.ballElapsed <= 0.0:
            ballmove = ballMovement(self.maze, self.speed, self.ballOri, self.ballGridX, self.ballGridZ)
            if ballmove[1] == "north": self.ballGridZ += 1
            if ballmove[1] == "south": self.ballGridZ -= 1
            if ballmove[1] == "east": self.ballGridX += 1
            if ballmove[1] == "west": self.ballGridX -= 1
            self.ballElapsed = ballmove[0]
            self.ballOri = ballmove[1]
            print(ballmove[0], ballmove[1], self.ballGridX, self.ballGridZ)
        if self.ballOri == "north":
            self.ballPosZ += (self.speed * delta_time) / 3.0
        if self.ballOri == "south":
            self.ballPosZ -= (self.speed * delta_time) / 3.0
        if self.ballOri == "west":
            self.ballPosX -= (self.speed * delta_time) / 3.0
        if self.ballOri == "east":
            self.ballPosX += (self.speed * delta_time) / 3.0
        self.ballCollision()
        self.playerMove(delta_time)

    def ballCollision(self):
        ballVec = Vector(self.view_matrix.eye.x - self.ballPosX, 0.0, self.view_matrix.eye.z - self.ballPosZ)
        distance = ballVec.__len__()
        if distance < self.radius:
            self.sphereMatB = random.uniform(0,1)
            self.sphereMatG = random.uniform(0,1)
            self.sphereMatR = random.uniform(0,1)


    def playerMove(self, delta_time):
        eyePosX = (int)(self.view_matrix.eye.x + 2) // 3  
        eyePosZ = (int)(self.view_matrix.eye.z + 2) // 3
        if self.w_key_down: 
            self.view_matrix.slide(0, 0, -2 * delta_time)
            if not self.maze.cells[eyePosX][eyePosZ].south:
                if self.view_matrix.eye.z < ((3 * eyePosZ) - 0.5):
                    self.view_matrix.eye.z = ((3 * eyePosZ) - 0.5)
            if not self.maze.cells[eyePosX][eyePosZ].west:
                if self.view_matrix.eye.x < ((3 * eyePosX) - 0.5):
                    self.view_matrix.eye.x = ((3 * eyePosX) - 0.5)
            if eyePosZ == (self.maze.size - 1):
                if self.view_matrix.eye.z > ((3 * eyePosZ) + 0.5):
                    self.view_matrix.eye.z = ((3 * eyePosZ) + 0.5)
            elif not self.maze.cells[eyePosX][eyePosZ + 1].south:
                if self.view_matrix.eye.z > ((3 * eyePosZ) + 0.5):
                    self.view_matrix.eye.z = ((3 * eyePosZ) + 0.5) 
            if eyePosX == (self.maze.size - 1):
                if self.view_matrix.eye.x > ((3 * eyePosX) + 0.5):
                    self.view_matrix.eye.x = ((3 * eyePosX) + 0.5)
            elif not self.maze.cells[eyePosX + 1][eyePosZ].west:
                if self.view_matrix.eye.x > ((3 * eyePosX) + 0.5):
                    self.view_matrix.eye.x = ((3 * eyePosX) + 0.5) 
        if self.s_key_down:
            self.view_matrix.slide(0, 0, 1 * delta_time)
            if not self.maze.cells[eyePosX][eyePosZ].south:
                if self.view_matrix.eye.z < ((3 * eyePosZ) - 0.5):
                    self.view_matrix.eye.z = ((3 * eyePosZ) - 0.5)
            if not self.maze.cells[eyePosX][eyePosZ].west:
                if self.view_matrix.eye.x < ((3 * eyePosX) - 0.5):
                    self.view_matrix.eye.x = ((3 * eyePosX) - 0.5)
            if eyePosZ == (self.maze.size - 1):
                if self.view_matrix.eye.z > ((3 * eyePosZ) + 0.5):
                    self.view_matrix.eye.z = ((3 * eyePosZ) + 0.5)
            elif not self.maze.cells[eyePosX][eyePosZ + 1].south:
                if self.view_matrix.eye.z > ((3 * eyePosZ) + 0.5):
                    self.view_matrix.eye.z = ((3 * eyePosZ) + 0.5) 
            if eyePosX == (self.maze.size - 1):
                if self.view_matrix.eye.x > ((3 * eyePosX) + 0.5):
                    self.view_matrix.eye.x = ((3 * eyePosX) + 0.5)
            elif not self.maze.cells[eyePosX + 1][eyePosZ].west:
                if self.view_matrix.eye.x > ((3 * eyePosX) + 0.5):
                    self.view_matrix.eye.x = ((3 * eyePosX) + 0.5)
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
        self.shader.set_light_position(Point(1.0, 1.0, 1.0))
        self.shader.set_light_diffuse(0.8, 0.3, 0.4)
        self.shader.set_light_specular(0.8, 0.3, 0.4)
        self.shader.set_light_ambiance(0.1, 0.1, 0.1)

        self.shader.set_light1_position(Point(1.0, 1.0, 1.0))
        self.shader.set_light1_diffuse(0.3, 0.6, 0.2)
        self.shader.set_light1_specular(0.8, 0.3, 0.4)
        self.shader.set_light1_ambiance(0.1, 0.1, 0.1)

        self.shader.set_light2_direction(Point(0.0, -1.0, 0.0))
        self.shader.set_light2_diffuse(0.4, 0.8, 0.8)
        self.shader.set_light2_specular(0.6, 0.3, 0.4)
        self.shader.set_light2_ambiance(0.1, 0.0, 0.0)
        self.drawSphere()
        self.displayMaze()
        self.drawExtirior()

        #floor
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(8.0, -0.2, 8.0)  
        self.model_matrix.add_scale(32.0, 0.4, 32.0)  
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_shininess(2)
        self.cube.set_vertices(self.shader)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()
        #pygame.display.flip()
        glViewport(400, 300, 600, 500) ##minimap
        glClear(GL_DEPTH_BUFFER_BIT)

        self.model_matrix.load_identity()        
        #self.cube.set_vertices(self.shaderself.shader)
        self.view_matrix_mini.look(self.view_matrix.eye + Point(0, 25, 10), self.view_matrix.eye + Point(0, 0, 10), Vector(0, 0, 1))
        self.shader.set_view_matrix(self.view_matrix_mini.get_matrix())
        self.shader.set_eye_position(self.view_matrix_mini.eye)

        self.drawSphere()
        self.displayMaze()
        self.drawExtirior()

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)  
        self.shader.set_material_diffuse(0.4, 0.9, 0.2)
        #self.model_matrix.add_scale(20.0, 0.4, 20.0)  
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.set_vertices(self.shader)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()
        
        #floor        
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(6.0, -0.2, 6.0)  
        self.model_matrix.add_scale(24.0, 0.4, 24.0)  
        self.shader.set_material_diffuse(0.2, 0.2, 0.2)
        self.shader.set_material_specular(0.1, 0.1, 0.1)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.shader.set_material_shininess(10)
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
    def displayMaze(self):
        for i in range (self.maze.size):
            for j in range (self.maze.size):
                if self.maze.cells[i][j].south == False:
                    self.drawSouthWall(i, j)
                if self.maze.cells[i][j].west == False:
                    self.drawWestWall(i, j)

    def drawWestWall(self, x, z):
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(3.0, 3.0, 3.0)
        self.model_matrix.add_translation(x - 0.5 , 1, z)
        self.model_matrix.add_scale(0.1, 2, 1)
        self.shader.set_material_diffuse(0.1, 0.1, 0.9)
        self.shader.set_material_specular(0.2,0.2,0.2)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.set_vertices(self.shader)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    def drawSouthWall(self, x, z):
        self.model_matrix.push_matrix()
        self.model_matrix.add_scale(3.0, 3.0, 3.0)
        self.model_matrix.add_translation(x , 1 , z - 0.5)
        self.model_matrix.add_scale(1, 2, 0.1)
        self.shader.set_material_diffuse(0.1, 0.1, 0.9)
        self.shader.set_material_specular(0.2,0.2,0.2)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.cube.set_vertices(self.shader)
        self.cube.draw(self.shader)
        self.model_matrix.pop_matrix()

    def drawExtirior(self):
        for i in range(self.size):
            self.drawSouthWall(i, self.size)
            self.drawWestWall(self.size, i)
    
    def drawSphere(self):
        self.sphere.set_vertices(self.shader)
        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.ballPosX, 1.0, self.ballPosZ)
        self.shader.set_material_diffuse(self.sphereMatR, self.sphereMatG, self.sphereMatB)
        self.shader.set_material_specular(0.4, 0.4, 0.4)
        self.shader.set_model_matrix(self.model_matrix.matrix)
        self.sphere.draw(self.shader)
        self.model_matrix.pop_matrix()

    def start(self):
        self.program_loop()

if __name__ == "__main__":
    GraphicsProgram3D().start()