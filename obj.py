from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
import numpy as np
import math

class object:
    def __init__(self):
        self.file_path : str = ""
        self.vertices : list[tuple[float, float, float]] = []
        self.faces : list[tuple[list[int], list[int]]] = []
        self.texture_coords : list[tuple[float, float]] = []
        self.mtl_coords : list[float] = []
        self.color_coords : list[float] = []
        self.x : float = 0.0
        self.y : float = 0.0
        self.z : float = 0.0
        self.texture_id : int = None
        self.frameNum = 0

    def __del__(self):
        if self.texture_id:
            glDeleteTextures([self.texture_id])        

    def load_file(self, file_path : str) -> None:
        with open(file_path, 'r') as f:
            for line in f:
                if line.startswith('v '):
                    parts = line.split()
                    self.vertices.append((float(parts[1]), float(parts[2]), float(parts[3])))
                elif line.startswith('vt '):
                    parts = line.split()
                    self.texture_coords.append((float(parts[1]), float(parts[2])))
                elif line.startswith('f '):
                    parts = line.split()
                    face = [int(part.split('/')[0]) - 1 for part in parts[1:]]
                    tex_face = [int(part.split('/')[1]) - 1 for part in parts[1:]]
                    self.faces.append((face, tex_face))

    def scale_texture(self, scale=1.0):
        scaled_coords = [(u * scale, v * scale) for u, v in self.texture_coords]
        self.texture_coords = scaled_coords

    def load_texture(self, texture_path: str) -> None:
        """Load a texture from a TGA file."""
        image = Image.open(texture_path)
        image = image.convert("RGB")

        width, height = image.size
        image_data = image.tobytes("raw", "RGB", 0, -1)

        glEnable(GL_TEXTURE_2D)
        self.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_id)

        # Set texture parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, image_data)

    def draw(self):
        if self.texture_coords and self.texture_id is not None:
            # Bind the texture if texture coordinates and texture ID are available
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glBegin(GL_TRIANGLES)
            for face, tex_face in self.faces:
                for i, vertex_idx in enumerate(face):
                    glTexCoord2fv(self.texture_coords[tex_face[i]])  # Texture coordinate
                    glVertex3fv(self.vertices[vertex_idx])  # Vertex position
            glEnd()
        else:
            # No texture; use color data if available
            glBegin(GL_TRIANGLES)
            for face, _ in self.faces:
                for vertex_idx in face:
                    if self.color_coords:  # Check for color data
                        glColor3fv(self.color_coords[vertex_idx])  # Apply color to the entire model
                    glVertex3fv(self.vertices[vertex_idx])  # Vertex position
            glEnd()

    def translate_draw(self, cor = None, rot = None):
        if cor is not None and rot is not None:
            glPushMatrix()
            if len(cor) == 3:
                glTranslatef(cor[0],cor[1],cor[2])
            if len(rot) == 4:
                glRotatef(rot[0],rot[1],rot[2],rot[3])
            self.draw()
            glPopMatrix()
    
    def texture_para(self,name):
        if name == 'oak':
            self.load_texture('textures/oak.png')
        elif name == 'birch':
            self.load_texture('textures/birch.png')
        elif name == 'spruce':
            self.load_texture('textures/spruce.png')
        else:
            self.load_texture('textures/oak.png')
    
    def hierarchyWheel(self,x,y,z,axis):
        numx = 0
        numy = 0
        numz = 0
        numv = 0
        
        for vertex_id in self.vertices: #finds center of obj
            numx += vertex_id[0]
            numy += vertex_id[1]
            numz += vertex_id[2]
            numv += 1
        numx = numx / numv
        numy = numy / numv
        numz = numz / numv

        glTranslatef(x,y,z)
        glTranslatef(numx,numy,numz)
        if axis == 0: #x_axis
            glRotatef(self.frameNum*2, 1, 0, 0)
        elif axis == 1: #y_axis
            glRotatef(self.frameNum*2, 0, 1, 0)
        elif axis == 2: #z_axis
            glRotatef(self.frameNum*2, 0, 0, 1)
        glTranslatef(-numx,-numy,-numz)
        self.draw()
        
        self.frameNum += 1
        if self.frameNum >= 180:
            self.frameNum = 0
    
    def hierarchyDropper(self,x,y,z):
        glTranslatef(x,self.frameNum,z)
        self.draw()
        
        self.frameNum += 1
        if self.frameNum >= 6:
            self.frameNum = 0.5
            

    
    def scale(self, x=1.0, y=1.0, z=1.0):
        self.vertices = [(vx * x, vy * y, vz * z) for vx, vy, vz in self.vertices]
    
    def fit_texture(self, texture_path: str):
        # Load the texture
        self.load_texture(texture_path)

        # Calculate the dimensions of the 3D object's bounding box
        min_x = min(v[0] for v in self.vertices)
        max_x = max(v[0] for v in self.vertices)
        min_y = min(v[1] for v in self.vertices)
        max_y = max(v[1] for v in self.vertices)
        min_z = min(v[2] for v in self.vertices)
        max_z = max(v[2] for v in self.vertices)

        width = max_x - min_x
        height = max_y - min_y
        depth = max_z - min_z

        # Prevent division by zero
        scale_x = 1.0 / width if width != 0 else 1.0
        scale_y = 1.0 / height if height != 0 else 1.0
        scale_z = 1.0 / depth if depth != 0 else 1.0

        # Recompute texture coordinates for 3D surfaces
        scaled_coords = []
        for vertex in self.vertices:
            u = (vertex[0] - min_x) * scale_x  # Map x-coordinates to u
            v = (vertex[1] - min_y) * scale_y  # Map y-coordinates to v
            w = (vertex[2] - min_z) * scale_z  # Map z-coordinates to w (optional)

            # Here we use the (u, w) coordinates, as OpenGL works with 2D texture coordinates.
            # You could alternatively use (u, v) or any combination depending on your mapping needs.
            scaled_coords.append((u, w))

        # Update texture coordinates
        self.texture_coords = scaled_coords

    def swept_elbow(self, radius, length, angle, segments):
        self.vertices = []
        self.faces = []

        # Calculate the angle step
        angle_step = angle / segments
        length_step = length / segments

        # Generate vertices
        for i in range(segments + 1):
            theta = math.radians(i * angle_step)
            for j in range(segments + 1):
                phi = math.radians(j * 360 / segments)
                x = radius * math.cos(phi)
                y = radius * math.sin(phi)
                z = length_step * i
                self.vertices.append((x, y, z))

        # Generate faces
        for i in range(segments):
            for j in range(segments):
                current = i * (segments + 1) + j
                next = current + 1
                next_ring = (i + 1) * (segments + 1) + j
                next_ring_next = next_ring + 1
                self.faces.append(([current, next, next_ring], []))
                self.faces.append(([next, next_ring_next, next_ring], []))
    
    def draw_cylinder(self, radius, height, segments):
        glBegin(GL_QUAD_STRIP)
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, 0)
            glVertex3f(x, y, height)
        glEnd()

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, 0)
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, 0)
        glEnd()

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0, 0, height)
        for i in range(segments + 1):
            angle = 2 * math.pi * i / segments
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            glVertex3f(x, y, height)
        glEnd()

    def draw_elbow(self, radius, length, angle, segments):
        self.swept_elbow(radius, length, angle, segments)
        self.draw()

    def translate_draw_elbow(self, cor=None, rot=None, radius=1, length=1, angle=90, segments=20):
        self.swept_elbow(radius, length, angle, segments)
        glPushMatrix()
        if cor and len(cor) == 3:
            glTranslatef(cor[0], cor[1], cor[2])
        if rot and len(rot) == 4:
            glRotatef(rot[0], rot[1], rot[2], rot[3])
        self.draw()
        # Draw cylinders at each end
        glPushMatrix()
        glTranslatef(0, 0, -length)
        self.draw_cylinder(radius, length, segments)
        glPopMatrix()
        glPushMatrix()
        glTranslatef(0, 0, length)
        self.draw_cylinder(radius, length, segments)
        glPopMatrix()
        glPopMatrix()

    def subdivide(self):
        new_vertices = []
        new_faces = []
        edges = {}

        def get_edge_key(v1, v2):
            return tuple(sorted((v1, v2)))

        def get_edge_vertex(v1, v2):
            edge_key = get_edge_key(v1, v2)
            if edge_key in edges:
                return edges[edge_key]
            else:
                new_vertex = (
                    (self.vertices[v1][0] + self.vertices[v2][0]) / 2,
                    (self.vertices[v1][1] + self.vertices[v2][1]) / 2,
                    (self.vertices[v1][2] + self.vertices[v2][2]) / 2
                )
                # Normalize the new vertex to lie on the surface of a sphere
                length = math.sqrt(new_vertex[0]**2 + new_vertex[1]**2 + new_vertex[2]**2)
                if length != 0:
                    new_vertex = (new_vertex[0] / length, new_vertex[1] / length, new_vertex[2] / length)
                new_vertices.append(new_vertex)
                edges[edge_key] = len(self.vertices) + len(new_vertices) - 1
                return edges[edge_key]

        for face, tex_face in self.faces:
            v0, v1, v2 = face
            a = get_edge_vertex(v0, v1)
            b = get_edge_vertex(v1, v2)
            c = get_edge_vertex(v2, v0)

            new_faces.append(([v0, a, c], []))
            new_faces.append(([v1, b, a], []))
            new_faces.append(([v2, c, b], []))
            new_faces.append(([a, b, c], []))

        self.vertices.extend(new_vertices)
        self.faces = new_faces
    def normalize_to_sphere(self):
        for i, vertex in enumerate(self.vertices):
            length = math.sqrt(vertex[0]**2 + vertex[1]**2 + vertex[2]**2)
            if length != 0:
                self.vertices[i] = (vertex[0] / length, vertex[1] / length, vertex[2] / length)
