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
from Car import *
from obj_3D_loading import *
from CarPhysics import *
from CarSimple import *
from RaceTrack import *
from DrawStuff import *

#from playsound import playsound

class GraphicsProgram3D:
    def __init__(self):

        pygame.init()
        pygame.display.set_mode((800,600), pygame.OPENGL|pygame.DOUBLEBUF)

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

        self.tree = load_obj_file(sys.path[0] + "/models" , "birch_tree.obj")
#        self.grass = load_obj_file(sys.path[0] + "/models" , "Grass.obj")
        self.test = load_obj_file(sys.path[0] + "/models" , "test2.obj")

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

        self.shader.set_light_position(Point(10.0, 10.0, 5.0))
        self.shader.set_light_diffuse(1.0, 1.0, 1.0)
        self.shader.set_light_specular(0.1, 0.8, 0.1)
        self.shader.set_light_ambiance(0.0, 0.0, 0.0)

        ##textures
        self.texture_id_skysphere = self.load_texture(sys.path[0] + "/textures/skysphere.jpg")

        #could leave empty for less detail
        self.skysphere = SkySphere(256, 512)

        self.track = RaceTrack(0.1, Point(0.0, 1.0, 0.0), Point(5.0, 1.0, 10.0), Point(10.0, 1.0, 10.0), Point(15.0, 1.0, 0.0))
        #playerone
        self.carSimple1 = CarSimple(Vector(0,1,5))
        #playertwo
        self.carSimple2 = CarSimple(Vector(0,1,0))
        self.white_background = False

    def update(self):
        delta_time = self.clock.tick() / 1000.0
        self.carSimpleMove1(delta_time)
        self.carSimpleMove2(delta_time)
        self.carSimple1.update(delta_time)
        self.carSimple2.update(delta_time)
        # print("car 1 position: ",self.carSimple1.position.x, self.carSimple1.position.y, self.carSimple1.position.z)
        # print("car 2 position: ", self.carSimple2.position.x, self.carSimple2.position.y, self.carSimple2.position.z )
        print("car 1 head: ", self.carSimple1.carHeading)
        print("car 2 head: ", self.carSimple2.carHeading)

    def display(self):
        glEnable(GL_DEPTH_TEST)  ### --- NEED THIS FOR NORMAL 3D BUT MANY EFFECTS BETTER WITH glDisable(GL_DEPTH_TEST) ... try it! --- ###

        if self.white_background:
            glClearColor(1.0, 1.0, 1.0, 1.0)
        else:
            glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)  ### --- YOU CAN ALSO CLEAR ONLY THE COLOR OR ONLY THE DEPTH --- ###

        #player 2 view, bottomhalf
        glViewport(0, 0, 800, 300)

        self.model_matrix.load_identity()
        self.view_matrix.look(Point(self.carSimple2.position.x + (sin(-self.carSimple2.carHeading) * 3), self.carSimple2.position.y + 1, self.carSimple2.position.z - (cos(-self.carSimple2.carHeading) * 3)), Point(self.carSimple2.position.x, self.carSimple2.position.y, self.carSimple2.position.z), Vector(0, 1, 0))
        
        ##important to draw skysphere first
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
        
        self.shader.use()
        #self.cube.set_vertices(self.shaderself.shader)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        self.shader.set_light_ambiance(0.1, 0.1, 0.1)

        #cube for now, will be a car later
        drawCar1(self)
        drawCar2(self)
        drawTree(self)
        drawTrack(self, self.track)

        #self.drawGrass()

        #drawfloor(self)       
       
       
        #player 1 view, tophalf
        glViewport(0, 300, 800, 300)

        self.model_matrix.load_identity()
        self.view_matrix.look(Point(self.carSimple1.position.x + (sin(-self.carSimple1.carHeading) * 3), (self.carSimple1.position.y + 1), self.carSimple1.position.z - (cos(-self.carSimple1.carHeading) * 3) ), Point(self.carSimple1.position.x, self.carSimple1.position.y, self.carSimple1.position.z), Vector(0, 1, 0))
        
        ##important to draw skysphere first
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
        
        self.shader.use()
        #self.cube.set_vertices(self.shaderself.shader)
        self.shader.set_view_matrix(self.view_matrix.get_matrix())
        self.shader.set_eye_position(self.view_matrix.eye)
        self.shader.set_light_ambiance(0.1, 0.1, 0.1)

        #cube for now, will be a car later
        
        drawCar2(self)
        drawCar1(self)
        drawTree(self)
        drawTrack(self, self.track)
        #self.drawGrass()

        #drawfloor(self)



        #important to only call flip() once, even though there are two viewports
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
                       # print("w key down")
                    elif event.key == K_s:
                        self.s_key_down = True
                      #  print("s key down")
                    elif event.key == K_a:
                        self.a_key_down = True
                       # print("a key down")
                    elif event.key == K_d:
                        self.d_key_down = True
                        #print("d key down")
                    elif event.key == K_LSHIFT:
                        self.LSHIFT_key_down = True
                    elif event.key == K_UP:
                        self.up_key_down = True
                       # print("up key down")
                    elif event.key == K_DOWN:
                        self.down_key_down = True
                       # print("down key down")
                    elif event.key == K_LEFT:
                        self.left_key_down = True
                        #print("left key down")
                    elif event.key == K_RIGHT:
                        self.right_key_down = True
                       # print("right key down")

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
            self.carSimple1.carSpeed += 10 * delta_time
            print("car1 w key down")
        if self.d_key_down:
            self.carSimple1.steerAngle -= (pi / 5 )* delta_time
            print("car1 d key down")
        if self.a_key_down:
            self.carSimple1.steerAngle += (pi / 5 )* delta_time
            print("car1 a key down")
        if not self.a_key_down and not self.d_key_down:
            self.carSimple1.steerAngle = 0
        if self.s_key_down:
            self.carSimple1.carSpeed -= 10 * delta_time
            print("car1 s key down")
      
        self.carSimple1.steerAngle = max(-self.carSimple1.maxSteerAngle, min(self.carSimple1.steerAngle, self.carSimple1.maxSteerAngle))
     
    def carSimpleMove2(self, delta_time): 
        #playertwo
        if self.up_key_down:
            self.carSimple2.carSpeed += 10 * delta_time
            print("car2 up key down")
        if self.right_key_down:
            self.carSimple2.steerAngle -= (pi / 5 )* delta_time
            print("car2 right key down")
        if self.left_key_down:
            self.carSimple2.steerAngle += (pi / 5 )* delta_time
            print("car2 left key down")
        if not self.left_key_down and not self.right_key_down:
            self.carSimple2.steerAngle = 0
        if self.down_key_down:
            self.carSimple2.carSpeed -= 10 * delta_time
            print("car2 down key down")
      
        self.carSimple2.steerAngle = max(-self.carSimple2.maxSteerAngle, min(self.carSimple2.steerAngle, self.carSimple2.maxSteerAngle))

if __name__ == "__main__":
    GraphicsProgram3D().start()