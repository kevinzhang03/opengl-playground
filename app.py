import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
import time
import math
import random

from Cube import Cube, Mesh
from Material import Material

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
        self.shader = self.create_shader('shaders/vertex.vert', 'shaders/fragment.frag')
        glUseProgram(self.shader)
        
        # Set texture unit 0 as active uniform sampler location for texture named 'imageTexture' in fragment shader
        glUniform1i(glGetUniformLocation(self.shader, 'imageTexture'), 0)
        
        # Define cube
        self.cube = Cube(
            position=[0, 0, -3],
            eulers=[0, 0, 0]
        )
        
        self.cube_mesh = Mesh('models/cube.obj')
        
        # Load texture image
        self.image_texture = Material('images/me.jpg')
        
        # Define a 4x4 projection transform with params
        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=APP_SIZE[0]/APP_SIZE[1], near=0.1, far=10, dtype=np.float32
        )
        
        #! add comment
        glUniformMatrix4fv(
            glGetUniformLocation(self.shader, 'projection'), 1, GL_FALSE, projection_transform
        )
        
        # Get location in shader where model matrix should go and stores it for efficiency
        self.model_matrix_location = glGetUniformLocation(self.shader, 'model')
        
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
            self.cube.eulers[2] += 1
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
            self.clock.tick(60)

        self.quit()

    def quit(self):
        self.cube_mesh.delete()
        self.image_texture.delete()
        glDeleteProgram(self.shader)
        pygame.quit()

if __name__ == '__main__':
    myApp = App()
