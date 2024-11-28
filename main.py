import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math
import obj
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

    return vertices, faces, texture_coords

def init_opengl(screen_width, screen_height):
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glDisable(GL_CULL_FACE)
    glClearColor(0.53, 0.81, 0.92, 1)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (screen_width / screen_height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def modify_texture_coords(texture_coords, scale=2.0):
    # Scale texture coordinates to make the texture repeat
    modified_coords = [(u * scale, v * scale) for u, v in texture_coords]
    return modified_coords

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

def draw_model(vertices, faces, texture_coords, texture_id):
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
    screen_width = 800
    screen_height = 600
    pygame.init()
    pygame.display.set_caption("Amusement Park Project")
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    init_opengl(screen_width, screen_height)

    object_1 = obj.object()
    object_1.load_file('MainPlatform.obj')
    object_1.scale_texture(20.0)
    object_1.load_texture('grass.tga')

    wall_mod = obj.object()
    wall_mod.load_file('wall.obj')
    wall_mod.color_coords = [184/255, 127/255, 66/255]

    object_2 = obj.object()
    object_2.load_file('ferris wheel.obj')
    object_2.scale_texture(1)
    object_2.load_texture('ferrisWheel.tga')

    # Camera parameters
    camera_radius = 40
    camera_angle_x = 45
    camera_angle_y = 0
    target_position = [0, 0, 0]  # Center of the object

    clock = pygame.time.Clock()
    running = True
    move_speed = 2  # Speed of movement

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    camera_radius -= 0.5
                elif event.button == 5:  # Scroll down
                    camera_radius += 0.5

        # Check the state of all keys
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            camera_angle_y -= move_speed
        if keys[K_RIGHT]:
            camera_angle_y += move_speed
        if keys[K_UP]:
            camera_angle_x -= move_speed
        if keys[K_DOWN]:
            camera_angle_x += move_speed
        if keys[K_w]:
            camera_radius -= 0.5
            if camera_radius < 2:
                camera_radius = 2
        if keys[K_s]:
            camera_radius += 0.5
        if keys[K_SPACE]:
            # Reset camera
            camera_radius = 20
            camera_angle_x = 45
            camera_angle_y = 45
        if keys[K_ESCAPE]:
            running = False

        # Clear and redraw
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Calculate camera position using spherical coordinates
        camera_x = camera_radius * math.sin(math.radians(camera_angle_y)) * math.cos(math.radians(camera_angle_x))
        camera_y = camera_radius * math.sin(math.radians(camera_angle_x))
        camera_z = camera_radius * math.cos(math.radians(camera_angle_y)) * math.cos(math.radians(camera_angle_x))

        # Set up the camera
        gluLookAt(
            camera_x, camera_y, camera_z,  # Camera position
            target_position[0], target_position[1], target_position[2],  # Look at the center of the object
            0, 1, 0  # Up direction
        )

        object_1.draw()
        wall_mod.translate_draw([19, 2.25, 0], [90, 0, 1, 0])
        object_2.translate_draw([3,0.3,3],[90,0,1,0])
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()