import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image  # For loading .tga texture files

def load_obj(file_path):
    vertices = []
    faces = []
    texture_coords = []

    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                parts = line.split()
                vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
            elif line.startswith('vt '):
                parts = line.split()
                texture_coords.append((float(parts[1]), float(parts[2])))
            elif line.startswith('f '):
                parts = line.split()
                face = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                tex_face = [int(part.split('/')[1]) - 1 for part in parts[1:]]
                faces.append((face, tex_face))

    return vertices, faces, normalize_texture_coords(texture_coords)

def normalize_texture_coords(texture_coords):
    min_u = min(tc[0] for tc in texture_coords)
    max_u = max(tc[0] for tc in texture_coords)
    min_v = min(tc[1] for tc in texture_coords)
    max_v = max(tc[1] for tc in texture_coords)

    u_range = max_u - min_u
    v_range = max_v - min_v

    # Normalize the texture coordinates to be within [0, 1]
    normalized_coords = [
        ((tc[0] - min_u) / u_range, (tc[1] - min_v) / v_range) for tc in texture_coords
    ]
    return normalized_coords

def load_tga_texture(texture_path):
    image = Image.open(texture_path)
    image = image.convert("RGB")
    
    width, height = image.size
    image_data = image.tobytes("raw", "RGB", 0, -1)

    glEnable(GL_TEXTURE_2D)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Set texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)  # Repeat horizontally
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)  # Repeat vertically

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    return texture_id

def modify_texture_coords(texture_coords, scale=2.0):
    # Scale texture coordinates to make the texture repeat
    modified_coords = [(u * scale, v * scale) for u, v in texture_coords]
    return modified_coords


def init_opengl():
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_CULL_FACE)
    glClearColor(0.5, 0.5, 0.5, 1)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (800 / 600), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def draw_model(vertices, faces, texture_coords, texture_id, rotation_x, rotation_y, zoom):
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -5 + zoom)  # Adjust position based on zoom

    # Apply rotations
    glRotatef(rotation_x, 1, 0, 0)
    glRotatef(rotation_y, 0, 1, 0)

    # Bind texture
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Draw model with texture
    glBegin(GL_TRIANGLES)
    for face, tex_face in faces:
        for i, vertex_idx in enumerate(face):
            glTexCoord2fv(texture_coords[tex_face[i]])
            glVertex3fv(vertices[vertex_idx])
    glEnd()

def main():
    pygame.init()
    pygame.display.set_caption("Amusement Park Project")
    pygame.display.set_mode((800, 600), DOUBLEBUF | OPENGL)
    init_opengl()

    # Load the model and texture
    vertices, faces, texture_coords = load_obj('MainPlatform.obj')
    texture_coords = modify_texture_coords(texture_coords, scale=2.0)  # Adjust the scale as desired
    texture_id = load_tga_texture('grass.tga')  # Path to your .tga texture file

    # Initialize rotation angles and zoom
    rotation_x, rotation_y = 0, 0
    zoom = 0

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    zoom += 0.5
                elif event.button == 5:  # Scroll down
                    zoom -= 0.5

        # Check the state of all keys
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            rotation_y -= 2
        if keys[K_RIGHT]:
            rotation_y += 2
        if keys[K_UP]:
            rotation_x -= 2
        if keys[K_DOWN]:
            rotation_x += 2
        if keys[K_w]:
            pass
        if keys[K_s]:
            pass
        if keys[K_a]:
            pass
        if keys[K_d]:
            pass
        if keys[K_SPACE]:
            pass

        # Clear and redraw
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_model(vertices, faces, texture_coords, texture_id, rotation_x, rotation_y, zoom)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
