import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from PIL import Image
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
                        glColor3fv(self.color_coords)  # Apply color to the entire model
                    glVertex3fv(self.vertices[vertex_idx])  # Vertex position
            glEnd()

    def translate_draw(self, cor = None, rot = None):
        if cor and rot:
            glPushMatrix()
            if len(cor) == 3:
                glTranslatef(cor[0],cor[1],cor[2])
            if len(rot) == 4:
                glRotatef(rot[0],rot[1],rot[2],rot[3])
            self.draw()
            glPopMatrix()

    def scale(self, x=1.0, y=1.0, z=1.0):
        self.vertices = [(vx * x, vy * y, vz * z) for vx, vy, vz in self.vertices]