import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
import time
import math
import random
import ctypes

APP_SIZE = (1280, 720)

class App:

    def __init__(self) -> None:
        # Initialize pygame
        pygame.init()
        pygame.display.set_mode((APP_SIZE[0], APP_SIZE[1]), pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        # Initialize OpenGL
        glClearColor(0.1, 0.1, 0.1, 1.0)
        
        # Enable and set up blending for transparency
        glEnable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Load and use shaders from files
        self.shader = self.create_shader("shaders/vertex.vert", "shaders/fragment.frag")
        glUseProgram(self.shader)
        
        # Set texture unit 0 as active uniform sampler location for texture named 'imageTexture' in fragment shader
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        
        # Define cube
        self.cube = Cube(
            position=[0, 0, -3],
            eulers=[0, 0, 0]
        )
        
        self.cube_mesh = CubeMesh()
        
        # Load texture image
        self.image_texture = Material("images/me.jpg")
        
        # Define a 4x4 projection transform with params
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=APP_SIZE[0]/APP_SIZE[1], near=0.1, far=10, dtype=np.float32
        )
        
        #! add comment
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, "projection"), 1, GL_FALSE, projection_transform
        )
        
        # Get location in shader where model matrix should go and stores it for efficiency
        self.model_matrix_location = glGetUniformLocation(self.shader, "model")
        
        self.main_loop()

    def create_shader(self, vertex_file_path, fragment_file_path):
        with open(vertex_file_path, 'r') as f:
            vertex_src = ''.join(f.readlines())
            
        with open(fragment_file_path, 'r') as f:
            fragment_src = ''.join(f.readlines())
            
        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )
        
        return shader

    def main_loop(self):
        start_time = time.time()
        running = True

        while running:
            # current_time = time.time() - start_time
            
            # Check events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            # Update cube
            self.cube.eulers[2] += 0.25
            if (self.cube.eulers[2] > 360):
                self.cube.eulers[2] -= 360

            # Refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Use shader program
            glUseProgram(self.shader)
            self.image_texture.use()
            
            # Create identity, multiply transformations progressively
            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            
            # Rotate cube around its own axis
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers),
                    dtype=np.float32
                )
            )
            
            # Translate cube to its position
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=self.cube.position,
                    dtype=np.float32
                )
            )
            
            glUniformMatrix4fv(self.model_matrix_location, 1, GL_FALSE, model_transform)
            
            glBindVertexArray(self.cube_mesh.vao)
            
            # Draw cube using currently bound shader and VAO
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)
            
            pygame.display.flip()

            # Timing
            self.clock.tick(360)

        self.quit()

    def quit(self):
        self.cube_mesh.delete()
        self.image_texture.delete()
        glDeleteProgram(self.shader)
        pygame.quit()

class Cube:
    
    def __init__(self, position, eulers) -> None:
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class CubeMesh:
    
    def __init__(self) -> None:# convert to type readable by graphics card
        # x, y, z, s, t
        self.vertices = np.array([
            -0.5, -0.5, -0.5, 0, 0,
             0.5, -0.5, -0.5, 1, 0,
             0.5,  0.5, -0.5, 1, 1,

             0.5,  0.5, -0.5, 1, 1,
            -0.5,  0.5, -0.5, 0, 1,
            -0.5, -0.5, -0.5, 0, 0,

            -0.5, -0.5,  0.5, 0, 0,
             0.5, -0.5,  0.5, 1, 0,
             0.5,  0.5,  0.5, 1, 1,

             0.5,  0.5,  0.5, 1, 1,
            -0.5,  0.5,  0.5, 0, 1,
            -0.5, -0.5,  0.5, 0, 0,

            -0.5,  0.5,  0.5, 1, 0,
            -0.5,  0.5, -0.5, 1, 1,
            -0.5, -0.5, -0.5, 0, 1,

            -0.5, -0.5, -0.5, 0, 1,
            -0.5, -0.5,  0.5, 0, 0,
            -0.5,  0.5,  0.5, 1, 0,

             0.5,  0.5,  0.5, 1, 0,
             0.5,  0.5, -0.5, 1, 1,
             0.5, -0.5, -0.5, 0, 1,

             0.5, -0.5, -0.5, 0, 1,
             0.5, -0.5,  0.5, 0, 0,
             0.5,  0.5,  0.5, 1, 0,

            -0.5, -0.5, -0.5, 0, 1,
             0.5, -0.5, -0.5, 1, 1,
             0.5, -0.5,  0.5, 1, 0,

             0.5, -0.5,  0.5, 1, 0,
            -0.5, -0.5,  0.5, 0, 0,
            -0.5, -0.5, -0.5, 0, 1,

            -0.5,  0.5, -0.5, 0, 1,
             0.5,  0.5, -0.5, 1, 1,
             0.5,  0.5,  0.5, 1, 0,

             0.5,  0.5,  0.5, 1, 0,
            -0.5,  0.5,  0.5, 0, 0,
            -0.5,  0.5, -0.5, 0, 1,
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

class Material:
    
    def __init__(self, filepath) -> None:
        # Generate texture ID and bind as 2D texture
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        
        # Set texture wrapping to repeat for S and T axes
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        # Set texture filtering (scaling), nearest for minimizing, linear for magnifying
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        # Load image and convert for OpenGL
        image = pygame.image.load(filepath).convert_alpha()
        image_width, image_height = image.get_rect().size
        image_data = pygame.image.tostring(image, "RGBA")
        
        # Create new texture from image data, setting it as the current texture of the bound texture object
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)
        
    def use(self):
        # Activate and bind the first texture unit
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        
    def delete(self):
        glDeleteTextures(1, (self.texture, ))

if __name__ == "__main__":
    myApp = App()
