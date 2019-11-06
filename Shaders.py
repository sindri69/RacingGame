from OpenGL.GL import *
from math import * # trigonometry

import sys

from Base3DObjects import *
from numpy import *



class Shader3D:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/simple3D.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)

        self.normalLoc = glGetAttribLocation(self.renderingProgramID, "a_normal")
        glEnableVertexAttribArray(self.normalLoc)
       

        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")
        
        self.eyePosLoc = glGetUniformLocation(self.renderingProgramID, "u_eye_position")
        self.lightPosLoc = glGetUniformLocation(self.renderingProgramID, "u_light_position")
        self.lightDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_light_diffuse")
        self.lightSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_light_specular")
        self.lightAmbianceLoc = glGetUniformLocation(self.renderingProgramID, "u_light_ambiance")

        self.materialDiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_material_diffuse")
        self.materialSpecLoc = glGetUniformLocation(self.renderingProgramID, "u_material_specular")
        self.materialShininessLoc = glGetUniformLocation(self.renderingProgramID, "u_material_shininess")
 
        self.light1PosLoc = glGetUniformLocation(self.renderingProgramID, "u_light1_position")
        self.light1DirLoc = glGetUniformLocation(self.renderingProgramID, "u_light1_direction")
        self.light1DiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_light1_diffuse")
        self.light1SpecLoc = glGetUniformLocation(self.renderingProgramID, "u_light1_specular")
        self.light1AmbianceLoc = glGetUniformLocation(self.renderingProgramID, "u_light1_ambiance")

   
        self.light2PosLoc = glGetUniformLocation(self.renderingProgramID, "u_light2_position")
        self.light2DirLoc = glGetUniformLocation(self.renderingProgramID, "u_light1_direction")
        self.light2DiffuseLoc = glGetUniformLocation(self.renderingProgramID, "u_light2_diffuse")
        self.light2SpecLoc = glGetUniformLocation(self.renderingProgramID, "u_light2_specular")
        self.light2AmbianceLoc = glGetUniformLocation(self.renderingProgramID, "u_light2_ambiance")
        


    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)
    
    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)
    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)
    
    def set_eye_position(self, pos):
        glUniform4f(self.eyePosLoc, pos.x, pos.y, pos.z, 1.0)

    def set_light_position(self, pos):
        glUniform4f(self.lightPosLoc, pos.x, pos.y, pos.z, 1.0)
    def set_light_diffuse(self, red, green, blue):
        glUniform4f(self.lightDiffuseLoc, red, green, blue, 1.0)
    def set_light_specular(self, red, green, blue):
        glUniform4f(self.lightSpecLoc, red, green, blue, 1.0)
    def set_light_ambiance(self, red, green, blue):
        glUniform4f(self.lightAmbianceLoc, red, green, blue, 1.0)


    def set_material_diffuse(self, color):
        glUniform4f(self.materialDiffuseLoc, color.r, color.g, color.b, 1.0)
    def set_material_specular(self, color):
        glUniform4f(self.materialSpecLoc, color.r, color.g, color.b, 1.0)
    def set_material_shininess(self, shininess):
        glUniform1f(self.materialShininessLoc, shininess)

    ##from the Shaders.py that came with MeshModelAddon
    def set_attribute_buffers(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 6 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))


    def set_position_attribute(self, vertex_array):
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 0, vertex_array)

    def set_normal_attribute(self, vertex_array):
        glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 0, vertex_array)



## this class is used for all texture mapping, not just the skysphere
class SkysphereShader:
    def __init__(self):
        vert_shader = glCreateShader(GL_VERTEX_SHADER)
        shader_file = open(sys.path[0] + "/skysphere_shader.vert")
        glShaderSource(vert_shader,shader_file.read())
        shader_file.close()
        glCompileShader(vert_shader)
        result = glGetShaderiv(vert_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile vertex shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(vert_shader)))

        frag_shader = glCreateShader(GL_FRAGMENT_SHADER)
        shader_file = open(sys.path[0] + "/skysphere_shader.frag")
        glShaderSource(frag_shader,shader_file.read())
        shader_file.close()
        glCompileShader(frag_shader)
        result = glGetShaderiv(frag_shader, GL_COMPILE_STATUS)
        if (result != 1): # shader didn't compile
            print("Couldn't compile fragment shader\nShader compilation Log:\n" + str(glGetShaderInfoLog(frag_shader)))

        self.renderingProgramID = glCreateProgram()
        glAttachShader(self.renderingProgramID, vert_shader)
        glAttachShader(self.renderingProgramID, frag_shader)
        glLinkProgram(self.renderingProgramID)

        self.positionLoc = glGetAttribLocation(self.renderingProgramID, "a_position")
        glEnableVertexAttribArray(self.positionLoc)


        self.uvLoc = glGetAttribLocation(self.renderingProgramID, "a_uv")
        glEnableVertexAttribArray(self.uvLoc)
       

        self.modelMatrixLoc			= glGetUniformLocation(self.renderingProgramID, "u_model_matrix")
        self.viewMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_view_matrix")
        self.projectionMatrixLoc = glGetUniformLocation(self.renderingProgramID, "u_projection_matrix")

        self.diffuseTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_tex01")
        self.alphaTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_tex02")

        self.opacityLoc = glGetUniformLocation(self.renderingProgramID, "u_opacity")
        #self.usingAlphaTextureLoc = glGetUniformLocation(self.renderingProgramID, "u_using_alpha_texture")
    
    def use(self):
        try:
            glUseProgram(self.renderingProgramID)   
        except OpenGL.error.GLError:
            print(glGetProgramInfoLog(self.renderingProgramID))
            raise

    def set_model_matrix(self, matrix_array):
        glUniformMatrix4fv(self.modelMatrixLoc, 1, True, matrix_array)
    
    def set_view_matrix(self, matrix_array):
        glUniformMatrix4fv(self.viewMatrixLoc, 1, True, matrix_array)
    
    def set_projection_matrix(self, matrix_array):
        glUniformMatrix4fv(self.projectionMatrixLoc, 1, True, matrix_array)
    
    def set_attribute_buffers_with_uv(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 5 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        #glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 5 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
    
    def set_attribute_buffers_with_uv_cube(self, vertex_buffer_id):
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_id)
        glVertexAttribPointer(self.positionLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(0))
        #glVertexAttribPointer(self.normalLoc, 3, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(3 * sizeof(GLfloat)))
        glVertexAttribPointer(self.uvLoc, 2, GL_FLOAT, False, 8 * sizeof(GLfloat), OpenGL.GLU.ctypes.c_void_p(6 * sizeof(GLfloat)))

    def set_diffuse_tex(self, number):
        glUniform1i(self.diffuseTextureLoc, number)

    def set_opacity(self, opacity):
        glUniform1f(self.opacityLoc, opacity)
    
    def set_alpha_tex(self, number):
        #glUniform1i(self.usingTextureLoc, 1.0)
        glUniform1i(self.alphaTextureLoc, number)
    # def set_spec_tex(self, number):
    #     glUniform1i(self.specularTextureLog, number)
    