from Base3DObjects import *

from OpenGL.GL import *
from OpenGL.GLU import *

import math
from math import *
import numpy


class RaceTrack:
    def __init__(self, halfwidth, p):
        t = 0.0
        norm = Point(0.0, 1.0, 0.0)
        self.vertexCount = 0
        vertex_arr = []
        pY = p[0].y
        pX = pow((1-t), 3) * p[0].x + 3 * t * pow((1-t), 2) * p[1].x + 3 * pow(t, 2) * (1 - t) * p[2].x + pow(t, 3) * p[3].x
        pZ = pow((1-t), 3) * p[0].z + 3 * t * pow((1-t), 2) * p[1].z + 3 * pow(t, 2) * (1 - t) * p[2].z + pow(t, 3) * p[3].z
        u = pow((1-t), 2) * (p[1].x - p[0].x) + 2 * t * (1-t) * (p[2].x - p[1].x) + pow(t, 2) * (p[3].x - p[2].x)
        v = pow((1-t), 2) * (p[1].z - p[0].z) + 2 * t * (1-t) * (p[2].z - p[1].z) + pow(t, 2) * (p[3].z - p[2].z)
        angle = atan2(u, v)
        pOutX = pX - cos(angle) * halfwidth
        pInX = pX + cos(angle) * halfwidth
        pOutZ = pZ + sin(angle) * halfwidth 
        pInZ = pZ - sin(angle) * halfwidth 
        while t < 1.0:
            pX = pow((1-t), 3) * p[0].x + 3 * t * pow((1-t), 2) * p[1].x + 3 * pow(t, 2) * (1 - t) * p[2].x + pow(t, 3) * p[3].x
            pZ = pow((1-t), 3) * p[0].z + 3 * t * pow((1-t), 2) * p[1].z + 3 * pow(t, 2) * (1 - t) * p[2].z + pow(t, 3) * p[3].z
            u = pow((1-t), 2) * (p[1].x - p[0].x) + 2 * t * (1-t) * (p[2].x - p[1].x) + pow(t, 2) * (p[3].x - p[2].x)
            v = pow((1-t), 2) * (p[1].z - p[0].z) + 2 * t * (1-t) * (p[2].z - p[1].z) + pow(t, 2) * (p[3].z - p[2].z)
            angle = atan2(u, v)
            pOutXnew = pX - cos(angle) * halfwidth
            pInXnew = pX + cos(angle) * halfwidth
            pOutZnew = pZ + sin(angle) * halfwidth 
            pInZnew = pZ - sin(angle) * halfwidth
            # print(pOutX, pOutZ)
            # print(pInX, pInZ)
            # print(pOutXnew, pOutZnew)
            # print(pInXnew, pInZnew)
            vertex_arr.extend([pOutX, pY, pOutZ, norm.x, norm.y, norm.z]) 
            vertex_arr.extend([pInX, pY, pInZ, norm.x, norm.y, norm.z]) 
            vertex_arr.extend([pOutXnew, pY, pOutZnew, norm.x, norm.y, norm.z]) 
            vertex_arr.extend([pInX, pY, pInZ, norm.x, norm.y, norm.z]) 
            vertex_arr.extend([pOutXnew, pY, pOutZnew, norm.x, norm.y, norm.z]) 
            vertex_arr.extend([pInXnew, pY, pInZnew, norm.x, norm.y, norm.z])
            self.vertexCount += 6
            pOutX = pOutXnew 
            pOutZ = pOutZnew 
            pInX = pInXnew 
            pInZ = pInZnew 
            t += 0.001
        self.vertex_buffer_id = glGenBuffers(1)        
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_arr, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        vertex_arr = None

    def draw(self, shader):
        shader.set_attribute_buffers(self.vertex_buffer_id)
        for i in range(0, self.vertexCount, 3):
            glDrawArrays(GL_TRIANGLES, i, 3)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
