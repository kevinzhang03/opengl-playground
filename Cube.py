from OpenGL.GL import *
from collections import defaultdict
import numpy as np
import ctypes

class Cube:
    
    def __init__(self, position, eulers) -> None:
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class Mesh:
    
    def __init__(self, filename) -> None:
        self.vertex_stride = 8
        self.v_data = defaultdict(list)
        
        # x, y, z, s, t, nx, ny, nz
        vertices = self.load_mesh(filename)
        self.vertex_count = len(vertices) // self.vertex_stride
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
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 4 * self.vertex_stride, ctypes.c_void_p(0))
        
        # Texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * self.vertex_stride, ctypes.c_void_p(12))
        
    def load_mesh(self, filename: str) -> list[float]:
        vertices = []
        
        with open(filename, 'r') as file:
            for line in file:
                words = line.strip().split()
                if words and words[0] in {'v', 'vt', 'vn'}:
                    self.v_data[words[0]].append(self.read_mesh_data(words))
                elif words and words[0] == 'f':
                    self.read_face_data(words, vertices)
        
        return vertices
    
    def read_mesh_data(self, words: list[str]) -> list[float]:
        return [float(word) for word in words[1:] if word]
    
    def read_face_data(self, words: list[str], vertices: list[float]) -> None:
        v  = self.v_data['v']
        vt = self.v_data['vt']
        vn = self.v_data['vn']
        
        """ Previous code:
        triangle_count = len(words) - 3
        
        for i in range(triangle_count):
            self.make_corner(words[1]    , v, vt, vn, vertices)
            self.make_corner(words[2 + i], v, vt, vn, vertices)
            self.make_corner(words[3 + i], v, vt, vn, vertices)
        """

        # Pre-process to extract all indices
        indices = [word.split('/') for word in words[1:]]
        
        # Validate indices and convert them to integers (assumes indices are complete and correct)
        indices = [(int(v_idx)-1 if v_idx else None, 
                    int(vt_idx)-1 if vt_idx else None, 
                    int(vn_idx)-1 if vn_idx else None) for v_idx, vt_idx, vn_idx in indices]

        # Each face is a polygon, triangulate the polygon by creating triangles from consecutive vertices
        for i in range(1, len(indices) - 1):
            for index_set in (indices[0], indices[i], indices[i + 1]):
                for idx, data_array in zip(index_set, (v, vt, vn)):
                    if idx is not None:  # Ensure the index is valid
                        vertices.extend(data_array[idx])
            
    def make_corner(
        self,
        corner: str,
        v: list[list[float]],
        vt: list[list[float]],
        vn: list[list[float]],
        vertices: list[float],
    ) -> None:
        
        """ Previous code:
        v_vt_vn = corner.split('/')
        for element in v[int(v_vt_vn[0]) - 1]:
            vertices.append(element)
        for element in vt[int(v_vt_vn[1]) - 1]:
            vertices.append(element)
        for element in vn[int(v_vt_vn[2]) - 1]:
            vertices.append(element)
        """

        v_idx, vt_idx, vn_idx = map(int, corner.split('/'))
        vertices.extend(v[v_idx - 1] + vt[vt_idx - 1] + vn[vn_idx - 1])
        
    def delete(self):
        glDeleteVertexArrays(1, (self.vao, ))
        glDeleteBuffers(1, (self.vbo, ))
