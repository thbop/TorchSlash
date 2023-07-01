from pyray import *


class spritesheet:
    def __init__(self, filename):
        self.sheet = load_image(filename)

        self.images = [self.sheet]
        self.textures = []

    def image_at(self, rec, key=Color(255, 255, 255, 255)):
        """
        Load a specific image from a specific rectangle
        Should NOT be run continuously (main loop), that will cause the memory to fill up... 
        """
        image = gen_image_color(int(rec.width), int(rec.height), WHITE)
        
        image_draw(image, self.sheet, rec, Rectangle(0, 0, rec.width, rec.height), WHITE)
        image_color_replace(image, key, Color(0, 0, 0, 0))
        self.images.append(image)
        texture = load_texture_from_image(image)
        self.textures.append(texture)
        return texture

    def unload(self):
        """
        Unload images and textures.
        Should run at the end of program
        """
        for i in self.images:
            unload_image(i)
        for t in self.textures:
            unload_texture(t)