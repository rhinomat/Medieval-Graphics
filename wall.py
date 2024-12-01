import obj
class wall(obj.object):
    def __init__(self, file_name, texture_name, sc_tex, sc_x, sc_y, sc_z):
        obj.object.__init__(self)
        self.load_file(file_name)
        self.load_texture(texture_name)
        self.scale_texture(sc_tex)
        self.scale(sc_x, sc_y, sc_z)
    