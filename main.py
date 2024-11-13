import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

def load_obj(file_path):
    vertices = []
    faces = []

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.split()
                vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif line.startswith('f '):
                parts = line.split()
                face = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                faces.append(face)
    
    return vertices, faces

def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glDisable(GL_LIGHTING)
    glClearColor(0.5, 0.5, 0.5, 1)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def draw_model(vertices, faces, rotation_x, rotation_y):
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5)
    
    # Apply rotations
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)

    # Draw filled model
    glColor3f(1.0, 0.5, 0.3)
    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex_idx in face:
            glVertex3fv(vertices[vertex_idx])
    glEnd()

    # Draw outline
    glColor3f(0, 0, 0)
    glLineWidth(1.5)

    for face in faces:
        glBegin(GL_LINE_LOOP)
        for vertex_idx in face:
            glVertex3fv(vertices[vertex_idx])
        glEnd()

def main():
    pygame.init()
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    init_opengl()

    vertices, faces = load_obj('base_platf_2.obj')
    rotation_x, rotation_y = 0, 0  # Initialize rotation angles

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

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_model(vertices, faces, rotation_x, rotation_y)
        pygame.display.flip()
        clock.tick(60)  # Run at 60 frames per second

    pygame.quit()

if __name__ == "__main__":
    main()
