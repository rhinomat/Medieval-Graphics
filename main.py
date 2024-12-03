import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import math
import obj
import wall
import roller_coaster

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
    object_1.load_file('objects/MainPlatform.obj')
    object_1.scale(2, 0, 2)
    object_1.scale_texture(20.0)
    object_1.load_texture('textures/grass.tga')

    track = roller_coaster.Track()
    track.initialize()

    wall_mod = wall.wall('objects/wall.obj', 'textures/worn_brick_floor_diff_4k.jpg', 2.0, 1, 0.5, 1)

    road_plat = obj.object()
    road_plat.load_file('objects/road_block.obj')
    road_plat.load_texture('textures/road_block.png')
    road_plat.scale(1, 1, 2)

    wheel = obj.object()
    wheel.load_file('objects/wheel.obj')
    wheel.scale_texture(1)
    wheel.load_texture('textures/wheel.png')
    wheel.scale(3,3,3)

    wheel_base = obj.object()
    wheel_base.load_file('objects/wheelBase.obj')
    wheel_base.scale_texture(1)
    wheel_base.load_texture('textures/wheelBase.png')
    wheel_base.scale(3,3,3)

    tree = obj.object()
    tree.load_file('objects/tree.obj')
    tree.scale_texture(1)
    tree.scale(2,2.5,2)

    entrance = obj.object()
    entrance.load_file('objects/entrance.obj')
    entrance.scale_texture(1)
    entrance.load_texture('textures/entrance.png')
    entrance.scale(1,1,1)

    exit = obj.object()
    exit.load_file('objects/exit.obj')
    exit.scale_texture(1)
    exit.load_texture('textures/exit.png')
    exit.scale(1,1,1)

    elbow = obj.object()    
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
        dt = clock.tick() / 1000.0
        track.update(dt)
        
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
        if keys[K_l]:
            pass
        if keys[K_m]:
            pass
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
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        object_1.draw()
        glPopMatrix()
        temp = wall_mod.vertices.copy()
        ticker = 0
        for i in range(-20, 20, 2):
            glPushMatrix()
            if ticker % 2 == 0:
                wall_mod.scale(1, 2, 1)
                glColor3f(1.0, 1.0, 1.0)
                wall_mod.translate_draw([i, 2.25, 20], [0, 0, 1, 0])
            else:
                wall_mod.vertices = temp.copy()
                glColor3f(1.0, 1.0, 1.0)
                wall_mod.translate_draw([i, 2.25 / 2, 20], [0, 0, 1, 0])
            glPopMatrix()
            ticker += 1

        for i in range(-20, 20, 2):
            glPushMatrix()
            if ticker % 2 == 0:
                wall_mod.scale(1, 2, 1)
                glColor3f(1.0, 1.0, 1.0)
                wall_mod.translate_draw([i, 2.25, -20], [0, 0, 1, 0])
            else:
                wall_mod.vertices = temp.copy()
                glColor3f(1.0, 1.0, 1.0)
                wall_mod.translate_draw([i, 2.25 / 2, -20], [0, 0, 1, 0])
            glPopMatrix()
            ticker += 1


        for i in range(-20, 20, 2):
            glPushMatrix()
            if i != 0: #ignores entrance and exit section
                if ticker % 2 == 0:
                    wall_mod.scale(1, 2, 1)
                    glColor3f(1.0, 1.0, 1.0)
                    wall_mod.translate_draw([20, 2.25, i], [90, 0, 1, 0])
                else:
                    wall_mod.vertices = temp.copy()
                    glColor3f(1.0, 1.0, 1.0)
                    wall_mod.translate_draw([20, 2.25 / 2, i], [90, 0, 1, 0])
            glPopMatrix()
            ticker += 1

        for i in range(-20, 20, 2):
            glPushMatrix()
            if ticker % 2 == 0:
                wall_mod.scale(1, 2, 1)
                glColor3f(1.0, 1.0, 1.0)
                wall_mod.translate_draw([-20, 2.25, i], [90, 0, 1, 0])
            else:
                wall_mod.vertices = temp.copy()
                glColor3f(1.0, 1.0, 1.0)
                wall_mod.translate_draw([-20, 2.25 / 2, i], [90, 0, 1, 0])
            glPopMatrix()
            ticker += 1

        for i in range(-20, 20, 2):
            glPushMatrix()
            glColor3f(1.0, 1.0, 1.0)
            road_plat.translate_draw([i, 0.001, 0], [90, 0, 1, 0])
            glPopMatrix()

        #ferris wheel
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        wheel.translate_draw([0,0.3,-15],[22.5,0,0,0])
        glPopMatrix()

        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        wheel_base.translate_draw([0,0.3,-15],[0,0,0,0])
        glPopMatrix()

        #parameterized trees
        tree.texture_para('birch')
        tree.translate_draw([-15,0.3,15],[0,0,0,0])
        tree.texture_para('oak')
        tree.translate_draw([15,0.3,15],[0,0,0,0])
        tree.texture_para('birch')
        tree.translate_draw([15,0.3,-15],[0,0,0,0])
        tree.texture_para('oak')
        tree.translate_draw([-15,0.3,-15],[0,0,0,0])
        tree.texture_para('spruce')
        tree.translate_draw([18,0.3,3],[0,0,0,0])
        tree.texture_para('spruce')
        tree.translate_draw([18,0.3,-3],[0,0,0,0])

        #entrance & exit
        entrance.translate_draw([19.5,0,0.5],[-90,0,1,0])
        exit.translate_draw([19.5,0,-0.5],[-90,0,1,0])
        
        
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        track.draw()
        glPopMatrix()
        glColor3f(1.0, 0.0, 0.0)
        elbow.translate_draw_elbow([0, 5, 0], [0, 90, 0, 1], radius=0.5, length=0.6, angle=45, segments=20)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()

if __name__ == "__main__":
    main()
