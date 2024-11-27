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
        """Render the object using OpenGL."""
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glBegin(GL_TRIANGLES)
        for face, tex_face in self.faces:
            for i, vertex_idx in enumerate(face):
                glTexCoord2fv(self.texture_coords[tex_face[i]])
                glVertex3fv(self.vertices[vertex_idx])
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

