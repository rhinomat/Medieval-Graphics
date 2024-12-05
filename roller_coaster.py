import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import math
import obj
class CubicBspline:
    def __init__(self, dim=3, loop=True, num=0, c_in=None):
        self.d = dim
        self.n = num
        self.loop = loop
        self.c_pts = None
        if c_in is not None:
            self.copy_controls(c_in)

    def copy_controls(self, c_in):
        self.c_pts = np.array(c_in, dtype=float)

    def evaluate_point(self, t):
        posn = int(math.floor(t))
        if posn > self.n - 4 and not self.loop:
            raise Exception("Parameter value out of range")

        u = t - posn
        u_sq = u * u
        u_cube = u * u_sq

        basis = np.array([
            -u_cube + 3.0 * u_sq - 3.0 * u + 1.0,
            3.0 * u_cube - 6.0 * u_sq + 4.0,
            -3.0 * u_cube + 3.0 * u_sq + 3.0 * u + 1.0,
            u_cube
        ]) / 6.0

        pt = np.zeros(self.d)
        for i in range(4):
            index = (posn + i) % self.n
            pt += self.c_pts[index] * basis[i]
        return pt

    def evaluate_derivative(self, t):
        posn = int(math.floor(t))
        if posn > self.n - 4 and not self.loop:
            raise Exception("Parameter value out of range")

        u = t - posn
        u_sq = u * u

        basis = np.array([
            -3.0 * u_sq + 6.0 * u - 3.0,
            9.0 * u_sq - 12.0 * u,
            -9.0 * u_sq + 6.0 * u + 3.0,
            3.0 * u_sq
        ]) / 6.0

        deriv = np.zeros(self.d)
        for i in range(4):
            index = (posn + i) % self.n
            deriv += self.c_pts[index] * basis[i]
        return deriv

    def append_control(self, pt):
        if self.c_pts is None:
            self.c_pts = np.array([pt], dtype=float)
        else:
            self.c_pts = np.vstack([self.c_pts, pt])
        self.n += 1

    def refine_tolerance(self, result, tolerance):
        self.refine(result)
        while not result.within_tolerance(tolerance):
            result.refine(result)

    def refine(self, result):
        new_n = self.n * 2 if self.loop else self.n * 2 - 3
        new_c = np.zeros((new_n, self.d))

        for i in range(0, new_n, 2):
            k = i // 2
            p0 = k % self.n
            p1 = (k + 1) % self.n
            p2 = (k + 2) % self.n

            new_c[i] = 0.5 * (self.c_pts[p0] + self.c_pts[p1])
            if i + 1 < new_n:
                new_c[i + 1] = 0.125 * (self.c_pts[p0] + 6.0 * self.c_pts[p1] + self.c_pts[p2])

        result.d = self.d
        result.n = new_n
        result.c_pts = new_c
        result.loop = self.loop

    '''def within_tolerance(self, tolerance):
        for i in range(self.n - 2):
            p1 = self.c_pts[i]
            p2 = self.c_pts[i + 1]
            p3 = self.c_pts[i + 2]

            x2_x1 = p2 - p1
            x3_x1 = p3 - p1
            l_13 = np.dot(x3_x1, x3_x1)
            if l_13 == 0.0:
                continue
            dot = np.dot(x2_x1, x3_x1)
            p = p1 + dot * x3_x1 / l_13
            l_2p = np.linalg.norm(p2 - p)
            if l_2p > tolerance:
                return False
        return True'''
    def within_tolerance(self, tolerance):
        for i in range(self.n - 2):
            p1 = self.c_pts[i]
            p2 = self.c_pts[i + 1]
            p3 = self.c_pts[i + 2]

            x2_x1 = p2 - p1
            x3_x1 = p3 - p1
            cross_product = np.cross(x2_x1, x3_x1)

            # Check if the cross product magnitude is within tolerance
            if np.linalg.norm(cross_product) > tolerance:
                return False
        return True


class Track:
    TRACK_NUM_CONTROLS = 4
    TRACK_CONTROLS = [
        [-20.0, -20.0, -18.0],
        [20.0, -20.0, 40.0],
        [20.0, 20.0, -18.0],
        [-20.0, 20.0, 40.0]
    ]
    TRAIN_ENERGY = 250.0

    def __init__(self):
        self.initialized = False
        self.posn_on_track = 0.0
        self.speed = 0.0
        self.track = None
        self.train_model = None

    def initialize(self):
        self.track = CubicBspline(3, True)
        for control in self.TRACK_CONTROLS:
            self.track.append_control(control)

        refined = CubicBspline(3, True)
        self.track.refine_tolerance(refined, 0.1)
        self.n_refined = refined.n

        self.track_list = glGenLists(1)
        glNewList(self.track_list, GL_COMPILE)
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)
        glPopMatrix()
        glPushMatrix()
        
        # Apply scaling
        glScalef(1, 1, 1)
        
        # Apply translation to move the track upward by 5 units
        glTranslatef(0, 0, 0)
        
        glBegin(GL_LINE_STRIP)
        for i in range(self.n_refined + 1):
            p = refined.evaluate_point(float(i))
            glVertex3fv(p)
        glEnd()
        glPopMatrix()
        glEndList()

        self.train_model = obj.object()
        self.train_model.load_file('objects/coaster_car.obj')
        glColor3f(0.0, 0.0, 0.0)

        self.train_model.load_texture('textures/coaster_car.png')

        self.train_list = glGenLists(1)
        '''glNewList(self.train_list, GL_COMPILE)
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_QUADS)
        self.draw_cube()
        glEnd()
        glEndList()'''

        self.initialized = True

    def draw_cube(self):
        vertices = [
            [0.5, 0.5, 1.0], [-0.5, 0.5, 1.0], [-0.5, -0.5, 1.0], [0.5, -0.5, 1.0],
            [0.5, -0.5, 0.0], [-0.5, -0.5, 0.0], [-0.5, 0.5, 0.0], [0.5, 0.5, 0.0]
        ]
        normals = [
            [0.0, 0.0, 1.0], [0.0, 0.0, -1.0], [1.0, 0.0, 0.0], [-1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0], [0.0, -1.0, 0.0]
        ]
        faces = [
            [0, 1, 2, 3], [4, 5, 6, 7], [0, 3, 4, 7], [1, 2, 5, 6], [0, 1, 6, 7], [2, 3, 4, 5]
        ]
        for i, face in enumerate(faces):
            glNormal3fv(normals[i])
            for vertex in face:
                glVertex3fv(vertices[vertex])

    def draw(self):
        if not self.initialized:
            return

        glPushMatrix()
        
        glCallList(self.track_list)
        glPopMatrix()

        glPushMatrix()
        glColor3f(1.0, 1.0, 1.0)  # White, for texture application

        # Bind the texture
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.train_model.texture_id)
        # Evaluate the model's position on the track
        posn = self.track.evaluate_point(self.posn_on_track)
        tangent = self.track.evaluate_derivative(self.posn_on_track)
        tangent = tangent / np.linalg.norm(tangent)

        angle1 = math.atan2(tangent[1], tangent[0]) * 180.0 / math.pi
        angle2 = math.asin(-tangent[2]) * 180.0 / math.pi


        # Draw the train model using translate_draw with combined rotation
        self.train_model.translate_draw(cor=posn, rot=(angle1, 0, 1.0, 1.0))

        glPopMatrix()

    def update(self, dt):
        if not self.initialized:
            return

        deriv = self.track.evaluate_derivative(self.posn_on_track)
        length = np.linalg.norm(deriv)
        if length == 0.0:
            return

        parametric_speed = self.speed / length
        self.posn_on_track += parametric_speed * dt

        if self.posn_on_track > self.track.n:
            self.posn_on_track -= self.track.n

        point = self.track.evaluate_point(self.posn_on_track)
        if self.TRAIN_ENERGY - 9.81 * point[2] < 0.0:
            self.speed = 0.0
        else:
            self.speed = math.sqrt(2.0 * (self.TRAIN_ENERGY - 9.81 * point[2]))
    
    def get_car_position(self):
        if not self.initialized:
            return None
        return self.track.evaluate_point(self.posn_on_track)
    def get_car_orientation(self):
        if not self.initialized:
            return None, None
        posn = self.track.evaluate_point(self.posn_on_track)
        tangent = self.track.evaluate_derivative(self.posn_on_track)
        tangent = tangent / np.linalg.norm(tangent)
        return posn, tangent