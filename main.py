import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def load_obj(file_path):
    vertices = []
    faces = []
    texture_coords = []

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):  # Vertex position
                parts = line.split()
                vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif line.startswith('vt '):  # Texture coordinate
                parts = line.split()
                texture_coords.append((float(parts[1]), float(parts[2])))
            elif line.startswith('f '):  # Face
                parts = line.split()
                face = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                tex_face = [int(part.split('/')[1]) - 1 for part in parts[1:]]
                faces.append((face, tex_face))

    return vertices, faces, texture_coords

def load_texture(texture_path):
    texture_surface = pygame.image.load(texture_path)
    texture_data = pygame.image.tostring(texture_surface, "RGB", 1)
    width, height = texture_surface.get_size()

    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    return texture_id

def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glClearColor(0.5, 0.5, 0.5, 1)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def draw_model(vertices, faces, texture_coords, texture_id, rotation_x, rotation_y):
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)

    # Apply rotations
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)

    # Bind texture
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Draw model with texture
    glBegin(GL_TRIANGLES)
    for face, tex_face in faces:
        for i, vertex_idx in enumerate(face):
            # Apply texture coordinate for each vertex
            glTexCoord2fv(texture_coords[tex_face[i]])
            glVertex3fv(vertices[vertex_idx])
    glEnd()

def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    init_opengl()

    # Load model and texture
    vertices, faces, texture_coords = load_obj('base_platf_2.obj')
    texture_id = load_texture('grass.tga')  # Replace with your texture image path

    # Initialize rotation angles
    rotation_x, rotation_y = 0, 0

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Check the state of all keys
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            rotation_y -= 2  # Rotate left continuously
        if keys[K_RIGHT]:
            rotation_y += 2  # Rotate right continuously
        if keys[K_UP]:
            rotation_x -= 2  # Rotate up continuously
        if keys[K_DOWN]:
            rotation_x += 2  # Rotate down continuously

        # Clear and redraw
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_model(vertices, faces, texture_coords, texture_id, rotation_x, rotation_y)
        pygame.display.flip()
        clock.tick(60)  # Run at 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
