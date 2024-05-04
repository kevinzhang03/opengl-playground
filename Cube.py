from OpenGL.GL import *
import numpy as np
import ctypes

class Cube:
    
    def __init__(self, position, eulers) -> None:
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class Mesh:
    
    def __init__(self, filename) -> None:
        # x, y, z, s, t, nx, ny, nz
        vertices = self.load_mesh(filename)
        self.vertex_count = len(vertices) // 8
        vertices = np.array(vertices, dtype=np.float32)
        
        # create VAO and VBO and binds them
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        # vertices
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        # Position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        
        # Texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))
        
    def load_mesh(self, filename: str) -> list[float]:
        v  = []
        vt = []
        vn = []
        
        vertices = []
        
        with open(filename, 'r') as file:
            for line in file:
                words = line.strip().split()
                if words and words[0] == 'v':
                    v.append(self.read_mesh_data(words))
                elif words and words[0] == 'vt':
                    vt.append(self.read_mesh_data(words))
                elif words and words[0] == 'vn':
                    vn.append(self.read_mesh_data(words))
                elif words and words[0] == 'f':
                    self.read_face_data(words, v, vt, vn, vertices)
                
        print(vertices)
        return vertices
    
    def read_mesh_data(self, words: list[str]) -> list[float]:
        return [float(word) for word in words[1:] if word]
    
    def read_face_data(
        self,
        words: list[str],
        v: list[list[float]],
        vt: list[list[float]],
        vn: list[list[float]],
        vertices: list[float],
    ) -> None:
        # Number of triangles in a face is always number of corners minus 2, and minus 'f'
        triangle_count = len(words) - 3
        
        for i in range(triangle_count):
            self.make_corner(words[1]    , v, vt, vn, vertices)
            self.make_corner(words[2 + i], v, vt, vn, vertices)
            self.make_corner(words[3 + i], v, vt, vn, vertices)
            
    def make_corner(
        self,
        corner: str,
        v: list[list[float]],
        vt: list[list[float]],
        vn: list[list[float]],
        vertices: list[float],
    ) -> None:
        v_vt_vn = corner.split('/')
        for element in v[int(v_vt_vn[0]) - 1]:
            vertices.append(element)
        for element in vt[int(v_vt_vn[1]) - 1]:
            vertices.append(element)
        for element in vn[int(v_vt_vn[2]) - 1]:
            vertices.append(element)
        
    def delete(self):
        # delete VAO and VBO
        glDeleteVertexArrays(1, (self.vao, ))
        glDeleteBuffers(1, (self.vbo, ))
