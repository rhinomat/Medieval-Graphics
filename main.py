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
    screen_width = 1280
    screen_height = 720
    pygame.init()
    pygame.display.set_caption("Amusement Park Project")
    screen = pygame.display.set_mode((screen_width, screen_height), DOUBLEBUF | OPENGL)
    init_opengl(screen_width, screen_height)

    object_1 = obj.object()
    object_1.load_file('objects/MainPlatform.obj')
    object_1.scale(2, 0, 2)
    object_1.scale_texture(100)
    object_1.load_texture('textures/grass.tga')

    track = roller_coaster.Track()
    track.initialize()
    track.speed = 0

    wall_short = wall.wall('objects/wall_short.obj', 'textures/Wall_short_paint.png', 1.0, 1, 1, 1)
    wall_tall = wall.wall('objects/wall_tall.obj', 'textures/wall_tall_paint.png', 1, 1, 1, 1)

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
    entrance.scale(0.5,0.5,0.5)

    exit = obj.object()
    exit.load_file('objects/exit.obj')
    exit.scale_texture(1)
    exit.load_texture('textures/exit.png')
    exit.scale(0.5,0.5,0.5)

    elbow = obj.object()    
    # Camera parameters
    camera_radius = 40
    camera_angle_x = 45
    camera_angle_y = 0
    target_position = [0, 0, 0]  # Center of the object

    clock = pygame.time.Clock()
    running = True
    move_speed = 2  # Speed of movement
    follow_car = False
    ride_mode = False
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    camera_radius -= 0.5
                elif event.button == 5:  # Scroll down
                    camera_radius += 0.5
        dt = clock.get_time() / 1000.0
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
            follow_car = not follow_car
        if keys[K_r]:
            ride_mode = not ride_mode
        if keys[K_SPACE]:
            # Reset camera
            camera_radius = 20
            camera_angle_x = 45
            camera_angle_y = 45
            follow_car = False
            ride_mode = False
        if keys[K_ESCAPE]:
            running = False

        # Clear and redraw
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        if ride_mode:
            # Get the car position and orientation
            car_position, car_tangent = track.get_car_orientation()
            if car_position is not None and car_tangent is not None:
                # Set the camera position to the car position
                camera_x, camera_y, camera_z = car_position

                # Calculate the look-at position based on the car's orientation
                look_at_x = camera_x + car_tangent[0]
                look_at_y = camera_y + car_tangent[1]
                look_at_z = camera_z + car_tangent[2]

                # Set up the camera
                gluLookAt(
                    camera_x, camera_y, camera_z,  # Camera position
                    look_at_x, look_at_y, look_at_z,  # Look at the direction of the car
                    0, 1, 0  # Up direction
                )
        else:
            if follow_car:
                car_position = track.get_car_position()
                if car_position is not None:
                    target_position = car_position

            # Calculate camera position using spherical coordinates
            camera_x = camera_radius * math.sin(math.radians(camera_angle_y)) * math.cos(math.radians(camera_angle_x)) + target_position[0]
            camera_y = camera_radius * math.sin(math.radians(camera_angle_x)) + target_position[1]
            camera_z = camera_radius * math.cos(math.radians(camera_angle_y)) * math.cos(math.radians(camera_angle_x)) + target_position[2]

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
        ticker = 0
        range_min = -19
        range_max = 19
        for i in range(range_min, range_max):
            glPushMatrix()
            if ticker % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)
                wall_tall.translate_draw([i, 0, 20], [180, 0, 1, 0])
            else:
                glColor3f(1.0, 1.0, 1.0)
                wall_short.translate_draw([i, 0, 20], [180, 0, 1, 0])
            glPopMatrix()
            ticker += 1

        for i in range(range_min, range_max):
            glPushMatrix()
            if ticker % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)
                wall_tall.translate_draw([i, 0, -20], [0, 0, 1, 0])
            else:
                glColor3f(1.0, 1.0, 1.0)
                wall_short.translate_draw([i, 0, -20], [0, 0, 1, 0])
            glPopMatrix()
            ticker += 1


        for i in range(range_min, range_max):
            glPushMatrix()
            if i != 0: #ignores entrance and exit section
                if ticker % 2 == 0:
                    glColor3f(1.0, 1.0, 1.0)
                    wall_tall.translate_draw([20, 0, i], [270, 0, 1, 0])
                else:
                    glColor3f(1.0, 1.0, 1.0)
                    wall_short.translate_draw([20, 0, i], [270, 0, 1, 0])
            glPopMatrix()
            ticker += 1

        for i in range(range_min, range_max):
            glPushMatrix()
            if ticker % 2 == 0:
                glColor3f(1.0, 1.0, 1.0)
                wall_tall.translate_draw([-20, 0, i], [90, 0, 1, 0])
            else:
                glColor3f(1.0, 1.0, 1.0)
                wall_short.translate_draw([-20, 0, i], [90, 0, 1, 0])
            glPopMatrix()
            ticker += 1

        for i in range(-20, 20):
            glPushMatrix()
            glColor3f(1.0, 1.0, 1.0)
            road_plat.translate_draw([i, 0.001, 0], [90, 0, 1, 0])
            glPopMatrix()

        corner = wall.wall('objects/corner.obj', 'textures/corner.png', 1, 1, 1, 1)
        corner.translate_draw([20, 0, 20], [0, 0, 0, 0])
        corner.translate_draw([20, 0, -20], [0, 0, 0, 0])
        corner.translate_draw([-20, 0, 20], [0, 0, 0, 0])
        corner.translate_draw([-20, 0, -20], [0, 0, 0, 0])


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
        tree.translate_draw([18,0.3,4],[0,0,0,0])
        tree.texture_para('spruce')
        tree.translate_draw([18,0.3,-4],[0,0,0,0])

        #entrance & exit
        entrance.translate_draw([19.5,0,0.25],[-90,0,1,0])
        exit.translate_draw([19.5,0,-0.25],[-90,0,1,0])
        
        
        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)
        track.draw()
        glPopMatrix()
        glColor3f(1.0, 1.0, 1.0)
        

        #arch sweep
        seg = 4
        rad = 3
        cylLen = 0.6
        cylRad = 0.5
        cylAng = 45
        cylSeg = 20
        
        th = math.pi / 2
        for i in range(seg):
            ang = (th / (seg-1)) * i
            nZ = rad * math.sin(ang)
            nY = rad * math.cos(ang) + 1.3
            elbow.translate_draw_elbow([15, nY, nZ], [math.degrees(ang), 1, 0, 0], cylRad, cylLen, cylAng, cylSeg)
            elbow.translate_draw_elbow([15, nY, -nZ], [-math.degrees(ang)-180, 1, 0, 0], cylRad, cylLen, cylAng, cylSeg)
        #end arch sweep
        glPushMatrix()
        glColor3f(1, 1, 1)
        wand_hand = obj.object()
        wand_hand.load_file('objects/wand_hand.obj')
        wand_hand.load_texture('textures/morph_wand_handle.png')
        wand_hand.scale(10, 10, 10)
        wand_hand.translate_draw([10, -2.5, 10], [0, 0, 0])
        glPopMatrix()
        #subdivision
        pyramid = obj.object()
        pyramid.load_file("objects/pyramid_sub.obj")
        #pyramid.load_texture("textures/pyramid.png")
        sign_post = obj.object()
        sign_post.load_file("objects/Sign_Post.obj")
        sign_post.load_texture("textures/sign_post.png")
        sign_post.translate_draw([12, 0, 5], [0, 0, 0, 0])
        keys = pygame.key.get_pressed()
        if keys[K_LALT]:
            pyramid.subdivide()
        glPushMatrix()
        glColor3f(1, 0, 1)      
        pyramid.translate_draw([10, 6.2, 6.2], [45, -1, 0, 0])
        glPopMatrix()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()

if __name__ == "__main__":
    main()
