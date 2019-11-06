from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import * #for the skybox
from math import *

import pygame
from pygame.locals import *

import sys
import time

from Shaders import *
from Matrices import *
from obj_3D_loading import *
from CarAI import *
from CarSimple import *
from RaceTrack import *
from DrawStuff import *


from playsound import playsound

class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((1200,900), pygame.OPENGL|pygame.DOUBLEBUF)

        self.shader = Shader3D()
        self.shader.use()

        self.model_matrix = ModelMatrix()

        self.view_matrix = ViewMatrix()
        self.view_matrix.look(Point(1, 3, -4), Point(0, 3, 1), Vector(0, 1, 0))
        self.projection_matrix = ProjectionMatrix()
        self.projection_matrix.set_perspective(pi/2, 8/3, 0.3, 30)
        self.shader.set_projection_matrix(self.projection_matrix.get_matrix())

        self.skysphere_shader = SkysphereShader()
        self.skysphere_shader.use()
        self.skysphere = SkySphere()
        
        self.shader.use()
        self.cube = Cube()
        self.cube.set_vertices(self.shader)
        self.textureCube = TextureCube()

        self.tree = load_obj_file(sys.path[0] + "/models" , "birch_tree.obj")
        #self.grass = load_obj_file(sys.path[0] + "/models" , "Grass.obj")
        self.test = load_obj_file(sys.path[0] + "/models" , "test2.obj")
        self.car_model = load_obj_file(sys.path[0] + "/models" , "shelby.obj")
        self.car_model2 = load_obj_file(sys.path[0] + "/models" , "shelby2.obj")
        self.car_model3 = load_obj_file(sys.path[0] + "/models" , "shelby3.obj")
        self.gate = load_obj_file(sys.path[0] + "/models" , "gate.obj")

        #playsound("./sounds/oh_yeah.mp3", False)

        self.clock = pygame.time.Clock()
        self.clock.tick()

        self.angle = 0

        #player one controls
        self.w_key_down = False
        self.s_key_down = False
        self.a_key_down = False
        self.d_key_down = False
        self.LSHIFT_key_down = False

        #player two controls
        self.up_key_down = False
        self.down_key_down = False
        self.left_key_down = False
        self.right_key_down = False

        self.shader.set_light_position(Point(0.0, 50.0, 100.0))
        self.shader.set_light_specular(0.1, 0.1, 0.1)
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_ambiance(0.1, 0.1, 0.1)

        ##textures
        self.texture_id_skysphere = self.load_texture(sys.path[0] + "/textures/skysphere.jpg")
        self.texture_id_grass = self.load_texture(sys.path[0] + "/textures/grass.jpg")


        #could leave empty for less detail
        self.skysphere = SkySphere(256, 512)
        self.onRoad1 = False
        self.onRoad2 = False
        self.bezierPoints = [Point(0.0, 1.0, 0.0), Point(10.0, 1.0, 25.0), Point(10.0, 1.0, 50.0), Point(-10.0, 1.0, 100.0), Point(10.0, 1.0, 150.0), Point(-10.0, 1.0, 200.0), Point(10.0, 1.0, 250.0), Point(-10.0, 1.0, 300.0), Point(10.0, 1.0, 350.0), Point(-10.0, 1.0, 400.0)]
        # bezierPoints2 = [Point(150.0, 1.0, 0.0), Point(50.0, 1.0, -100.0), Point(50.0, 1.0, -100.0), Point(0.0, 1.0, 0.0)]
        self.track = RaceTrack(10, self.bezierPoints, 30, 30, 60)
        # self.track2 = RaceTrack(10, bezierPoints2)
        self.carAI = CarAI(3.0, 15.0, self.bezierPoints)
        self.totalTime = 0.0
        #playerone
        self.carSimple1 = CarSimple(Vector(-2,1.2,5))
        #playertwo
        self.carSimple2 = CarSimple(Vector(2,1.2,5))
        self.white_background = False

        self.gameOver = False
        self.winner = ''
        self.messageNotPrinted = True


    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.totalTime += delta_time
        self.carSimpleMove1(delta_time)
        self.carSimpleMove2(delta_time)
        self.carSimple1.update(delta_time)
        self.carSimple2.update(delta_time)
        self.onRoad1 = self.track.grass(self.carSimple1)
        self.onRoad2 = self.track.grass(self.carSimple2)
        self.carAI.update(self.totalTime)
        self.gameOverPrompt()
        

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        #player 2 view, bottomhalf
        glViewport(0, 0, 1200, 450)

        self.model_matrix.load_identity()
        self.view_matrix.look(Point(self.carSimple2.position.x + (sin(-self.carSimple2.carHeading) * 3.5), self.carSimple2.position.y + 2, self.carSimple2.position.z - (cos(-self.carSimple2.carHeading) * 3.5)), Point(self.carSimple2.position.x, self.carSimple2.position.y, self.carSimple2.position.z), Vector(0, 1, 0))
        
        ##important to draw skysphere first
        self.displaySkysphere()

        self.shader.use()
        #self.cube.set_vertices(self.shaderself.shader)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        self.shader.set_light_ambiance(0.1, 0.1, 0.1)

        #cube for now, will be a car later
        drawCar1(self)
        drawCar2(self)
        drawCarAI(self)
        drawForrest(self)
        drawTrack(self, self.track)
        drawGates(self)
        drawGrass(self, self.carSimple2)

        #drawfloor(self)       
       
       
        #player 1 view, tophalf
        glViewport(0, 450, 1200, 450)

        self.model_matrix.load_identity()
        self.view_matrix.look(Point(self.carSimple1.position.x + (sin(-self.carSimple1.carHeading) * 3.5), (self.carSimple1.position.y + 2), self.carSimple1.position.z - (cos(-self.carSimple1.carHeading) * 3.5) ), Point(self.carSimple1.position.x, self.carSimple1.position.y, self.carSimple1.position.z), Vector(0, 1, 0))
        
        ##important to draw skysphere first
        self.displaySkysphere()
        
        self.shader.use()
        #self.cube.set_vertices(self.shaderself.shader)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        self.shader.set_light_ambiance(0.1, 0.1, 0.1)

        #cube for now, will be a car later
        
        drawCar2(self)
        drawCar1(self)
        drawCarAI(self)
        drawForrest(self)
        drawTree(self)
        drawTrack(self, self.track)
        drawGates(self)
        drawGrass(self, self.carSimple1)

        #drawfloor(self)



        #important to only call flip() once, even though there are two viewports
        pygame.display.flip()


    def program_loop(self):
        exiting = False
        while not exiting:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exiting = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                        exiting = True
                    if event.key == K_w:
                        self.w_key_down = True
                    elif event.key == K_s:
                        self.s_key_down = True
                    elif event.key == K_a:
                        self.a_key_down = True
                    elif event.key == K_d:
                        self.d_key_down = True
                    elif event.key == K_LSHIFT:
                        self.LSHIFT_key_down = True
                    elif event.key == K_UP:
                        self.up_key_down = True
                    elif event.key == K_DOWN:
                        self.down_key_down = True
                    elif event.key == K_LEFT:
                        self.left_key_down = True
                    elif event.key == K_RIGHT:
                        self.right_key_down = True
                    elif event.key == K_SPACE and self.gameOver:
                        self.restartGame()

                elif event.type == pygame.KEYUP:

                    if event.key == K_w:
                        self.w_key_down = False
                    elif event.key == K_s:
                        self.s_key_down = False
                    elif event.key == K_a:
                        self.a_key_down = False
                    elif event.key == K_d:
                        self.d_key_down = False
                    elif event.key == K_LSHIFT:
                        self.LSHIFT_key_down = False
                    elif event.key == K_UP:
                        self.up_key_down = False
                    elif event.key == K_DOWN:
                        self.down_key_down = False
                    elif event.key == K_LEFT:
                        self.left_key_down = False
                    elif event.key == K_RIGHT:
                        self.right_key_down = False

            self.update()
            self.display()

        #OUT OF GAME LOOP
        pygame.quit()

    def start(self):
        self.program_loop()
    
    def load_texture(self, path_string):
        surface = pygame.image.load(path_string)
        tex_string = pygame.image.tostring(surface, "RGBA", 1)
        width = surface.get_width()
        height = surface.get_height()
        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, tex_string)
        return tex_id

    def carSimpleMove1(self, delta_time):
        #playerone
        if self.w_key_down:
            if self.carSimple1.carSpeed < self.carSimple1.maxSpeed:
                self.carSimple1.carSpeed += 10 * delta_time
        if self.d_key_down:
            self.carSimple1.steerAngle -= (pi / 5 )* delta_time
        if self.a_key_down:
            self.carSimple1.steerAngle += (pi / 5 )* delta_time
        if not self.a_key_down and not self.d_key_down:
            self.carSimple1.steerAngle = 0
        if self.s_key_down:
            if self.carSimple1.carSpeed > self.carSimple1.maxBackSpeed:
                self.carSimple1.carSpeed -= 10 * delta_time
        self.carSimple1.steerAngle = max(-self.carSimple1.maxSteerAngle, min(self.carSimple1.steerAngle, self.carSimple1.maxSteerAngle))
        if not self.onRoad1 and self.carSimple1.carSpeed >= 20:
            self.carSimple1.carSpeed -= 50 * delta_time
            print(self.carSimple1.carSpeed)
    def carSimpleMove2(self, delta_time): 
        #playertwo
        if self.up_key_down:
            if self.carSimple2.carSpeed < self.carSimple2.maxSpeed:
                self.carSimple2.carSpeed += 10 * delta_time
        if self.right_key_down:
            self.carSimple2.steerAngle -= (pi / 5 )* delta_time
        if self.left_key_down:
            self.carSimple2.steerAngle += (pi / 5 )* delta_time
        if not self.left_key_down and not self.right_key_down:
            self.carSimple2.steerAngle = 0
        if self.down_key_down:
            if self.carSimple2.carSpeed > self.carSimple2.maxBackSpeed:
                self.carSimple2.carSpeed -= 10 * delta_time
        if not self.onRoad2 and self.carSimple2.carSpeed >= 20:
            self.carSimple2.carSpeed -= 20 * delta_time
      
        self.carSimple2.steerAngle = max(-self.carSimple2.maxSteerAngle, min(self.carSimple2.steerAngle, self.carSimple2.maxSteerAngle))
    
    def displaySkysphere(self):
        glDisable(GL_DEPTH_TEST)
        self.skysphere_shader.use()
        self.skysphere_shader.set_projection_matrix(self.projection_matrix.get_matrix())
        self.skysphere_shader.set_view_matrix(self.view_matrix.get_matrix())

        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture_id_skysphere)
        self.skysphere_shader.set_diffuse_tex(0)
        #self.skysphere_shader.set_alpha_tex(None)

        self.skysphere_shader.set_opacity(1.0)

        self.model_matrix.push_matrix()
        self.model_matrix.add_translation(self.view_matrix.eye.x, self.view_matrix.eye.y, self.view_matrix.eye.z)
        self.skysphere_shader.set_model_matrix(self.model_matrix.matrix)
        
        self.skysphere.draw(self.skysphere_shader)

        self.model_matrix.pop_matrix()
        
        glEnable(GL_DEPTH_TEST)

        glClear(GL_DEPTH_BUFFER_BIT) 
    
    def gameOverPrompt(self):
        if self.gameOver and self.messageNotPrinted:
            print("The game is over and the winner was ", self.winner, "! If you want to play again press the spacebar!")
            self.messageNotPrinted = False
        if (self.carSimple1.position - self.bezierPoints[-1]).__len__() < 2:
            self.winner = "Player one"
            self.gameOver = True
        elif (self.carSimple2.position - self.bezierPoints[-1]).__len__() < 2:
            self.winner = "Player two"
            self.gameOver = True
        elif self.totalTime > 10:
            self.winner = "the AI, you suck"
            self.gameOver = True
       
    
    def restartGame(self):
        self.carAI = CarAI(3.0, 15.0, self.bezierPoints)
        self.totalTime = 0.0
        #playerone
        self.carSimple1 = CarSimple(Vector(0,1.2,5))
        #playertwo
        self.carSimple2 = CarSimple(Vector(0,1.2,0))
        self.white_background = False
        self.messageNotPrinted = True

        self.gameOver = False
        self.winner = ''
if __name__ == "__main__":
    GraphicsProgram3D().start()