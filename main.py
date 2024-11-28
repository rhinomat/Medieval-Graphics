import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math
import obj

def init_opengl(screen_width, screen_height):
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LEQUAL)
    glDisable(GL_CULL_FACE)
    glClearColor(0.53, 0.81, 0.92, 1)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (screen_width / screen_height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def main():
    screen_width = 800
    screen_height = 600
    pygame.init()
    pygame.display.set_caption("Amusement Park Project")
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    init_opengl(screen_width, screen_height)

    object_1 = obj.object()
    object_1.load_file('MainPlatform.obj')
    object_1.scale(2, 1, 2);
    object_1.scale_texture(20.0)
    object_1.load_texture('grass.tga')

    wall_mod = obj.object()
    wall_mod.load_file('wall.obj')
    #wall_mod.color_coords = [151/255, 232/255, 210/255]
    wall_mod.load_texture('worn_brick_floor_diff_4k.jpg')
    wall_mod.scale_texture(2)

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
        temp = wall_mod.vertices.copy()
        ticker = 0
        for i in range(-20, 20, 2):
            if ticker % 2 == 0:
                wall_mod.scale(1, 2, 1)
                wall_mod.translate_draw([i, 2.25 * 2, 20], [0, 0, 1, 0])
            else:
                wall_mod.vertices = temp.copy()
                wall_mod.translate_draw([i, 2.25, 20], [0, 0, 1, 0])
            ticker += 1

        for i in range(-20, 20, 2):
            if ticker % 2 == 0:
                wall_mod.scale(1, 2, 1)
                wall_mod.translate_draw([i, 2.25 * 2, -20], [0, 0, 1, 0])
            else:
                wall_mod.vertices = temp.copy()
                wall_mod.translate_draw([i, 2.25, -20], [0, 0, 1, 0])
            ticker += 1


        for i in range(-20, 20, 2):
            if ticker % 2 == 0:
                wall_mod.scale(1, 2, 1)
                wall_mod.translate_draw([20, 2.25 * 2, i], [90, 0, 1, 0])
            else:
                wall_mod.vertices = temp.copy()
                wall_mod.translate_draw([20, 2.25, i], [90, 0, 1, 0])
            ticker += 1

        for i in range(-20, 20, 2):
            if ticker % 2 == 0:
                wall_mod.scale(1, 2, 1)
                wall_mod.translate_draw([-20, 2.25 * 2, i], [90, 0, 1, 0])
            else:
                wall_mod.vertices = temp.copy()
                wall_mod.translate_draw([-20, 2.25, i], [90, 0, 1, 0])
            ticker += 1

        object_2.translate_draw([3,0.3,3],[90,0,1,0])
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
