from OpenGL.GL import *
import numpy as np
import ctypes

class Cube:
    
    def __init__(self, position, eulers) -> None:
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class CubeMesh:
    
    def __init__(self) -> None:
        # x, y, z, s, t
        self.vertices = np.array([
            -0.5,  0.5, -0.5, 0, 0,
             0.5,  0.5, -0.5, 1, 0,
             0.5, -0.5, -0.5, 1, 1,

             0.5, -0.5, -0.5, 1, 1,
            -0.5, -0.5, -0.5, 0, 1,
            -0.5,  0.5, -0.5, 0, 0,

            -0.5,  0.5,  0.5, 0, 0,
             0.5,  0.5,  0.5, 1, 0,
             0.5, -0.5,  0.5, 1, 1,

             0.5, -0.5,  0.5, 1, 1,
            -0.5, -0.5,  0.5, 0, 1,
            -0.5,  0.5,  0.5, 0, 0,

            -0.5, -0.5,  0.5, 1, 0,
            -0.5, -0.5, -0.5, 1, 1,
            -0.5,  0.5, -0.5, 0, 1,

            -0.5,  0.5, -0.5, 0, 1,
            -0.5,  0.5,  0.5, 0, 0,
            -0.5, -0.5,  0.5, 1, 0,

             0.5, -0.5,  0.5, 1, 0,
             0.5, -0.5, -0.5, 1, 1,
             0.5,  0.5, -0.5, 0, 1,

             0.5,  0.5, -0.5, 0, 1,
             0.5,  0.5,  0.5, 0, 0,
             0.5, -0.5,  0.5, 1, 0,

            -0.5,  0.5, -0.5, 0, 1,
             0.5,  0.5, -0.5, 1, 1,
             0.5,  0.5,  0.5, 1, 0,

             0.5,  0.5,  0.5, 1, 0,
            -0.5,  0.5,  0.5, 0, 0,
            -0.5,  0.5, -0.5, 0, 1,

            -0.5, -0.5, -0.5, 0, 1,
             0.5, -0.5, -0.5, 1, 1,
             0.5, -0.5,  0.5, 1, 0,

             0.5, -0.5,  0.5, 1, 0,
            -0.5, -0.5,  0.5, 0, 0,
            -0.5, -0.5, -0.5, 0, 1,
        ], dtype=np.float32)
        
        self.vertex_stride = 5
        self.vertex_count = len(self.vertices) // 5
        
        # create VAO and VBO and binds them
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        
        # send the buffer vertex data to the VBO
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        
        # set up position attribute
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        
        # set up texture attribute
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
        
    def delete(self):
        # delete VAO and VBO
        glDeleteVertexArrays(1, (self.vao, ))
        glDeleteBuffers(1, (self.vbo, ))
