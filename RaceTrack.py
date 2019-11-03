from Base3DObjects import *

class RaceTrack:
    def __init__(self, halfwidth, p0, p1, p2, p3):
        t = 0.0
        norm = Point(0.0, 1.0, 0.0)
        vertex_arr = []
        pY = p0.y
        pX = pow((1-t), 3) * p0.x + 3 * t * pow((1-t), 2) * p1.x + 3 * pow(t, 2) * (1 - t) * p2.x + pow(t, 3) * p2.x
        pZ = pow((1-t), 3) * p0.z + 3 * t * pow((1-t), 2) * p1.z + 3 * pow(t, 2) * (1 - t) * p2.z + pow(t, 3) * p2.z
        u = pow((1-t), 2) * (p1.x - p0.x) + 2 * t * (1-t) * (p2.x - p1.x) + pow(t, 2) * (p3.x - p2.x)
        v = pow((1-t), 2) * (p1.z - p0.z) + 2 * t * (1-t) * (p2.z - p1.z) + pow(t, 2) * (p3.z - p2.z)
        angle = atan2(u, v)
        pOutX = pX - cos(angle) * halfwidth
        pInX = pX + cos(angle) * halfwidth
        pOutZ = pZ + sin(angle) * halfwidth 
        pInZ = pZ - sin(angle) * halfwidth 
        print(vertex_arr)
        while t < 1.0:
            pX = pow((1-t), 3) * p0.x + 3 * t * pow((1-t), 2) * p1.x + 3 * pow(t, 2) * (1 - t) * p2.x + pow(t, 3) * p2.x
            pZ = pow((1-t), 3) * p0.z + 3 * t * pow((1-t), 2) * p1.z + 3 * pow(t, 2) * (1 - t) * p2.z + pow(t, 3) * p2.z
            u = pow((1-t), 2) * (p1.x - p0.x) + 2 * t * (1-t) * (p2.x - p1.x) + pow(t, 2) * (p3.x - p2.x)
            v = pow((1-t), 2) * (p1.z - p0.z) + 2 * t * (1-t) * (p2.z - p1.z) + pow(t, 2) * (p3.z - p2.z)
            angle = atan2(u, v)
            pOutXnew = pX - cos(angle) * halfwidth
            pInXnew = pX + cos(angle) * halfwidth
            pOutZnew = pZ + sin(angle) * halfwidth 
            pInZnew = pZ - sin(angle) * halfwidth
            vertex_arr.extend([pOutX, pY, pOutZ, norm.x, norm.y, norm.z]) 
            vertex_arr.extend([pInX, pY, pInZ, norm.x, norm.y, norm.z]) 
            vertex_arr.extend([pOutXnew, pY, pOutZnew, norm.x, norm.y, norm.z]) 
            vertex_arr.extend([pInX, pY, pInZ, norm.x, norm.y, norm.z]) 
            vertex_arr.extend([pOutXnew, pY, pOutZnew, norm.x, norm.y, norm.z]) 
            vertex_arr.extend([pInXnew, pY, pOutZnew, norm.x, norm.y, norm.z])
            pOutX = pOutXnew 
            poutZ = pOutZnew 
            pInX = pInXnew 
            pInZ = pInZnew 
            t += 0.1
        self.vertex_buffer_id = glGenBuffers(1)        
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer_id)
        glBufferData(GL_ARRAY_BUFFER, numpy.array(vertex_arr, dtype='float32'), GL_STATIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        vertex_arr = None

    def draw(self, shader):
        shader.set_attribute_buffers(self.vertex_buffer_id)
        for i in range(0, self.vertex_count, (self.slices + 1) * 2):
            glDrawArrays(GL_TRIANGLE_STRIP, i, (self.slices + 1) * 2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)


track = RaceTrack(1, Point(0.0, 1.0, 0.0), Point(0.25, 1.0, 1.0), Point(0.75, 1.0, 1.0), Point(1.0, 1.0, 0.0))
