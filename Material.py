import pygame
from OpenGL.GL import *

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
