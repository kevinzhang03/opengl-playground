import pygame
from OpenGL.GL import glGetString, GL_VERSION

pygame.init()
screen = pygame.display.set_mode((640, 480), pygame.OPENGL | pygame.DOUBLEBUF)
print(glGetString(GL_VERSION))
pygame.quit()
