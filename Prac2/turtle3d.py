from vpython import *


class Turtle3D:
    """ Aquesta clase defineix l'objecte Turtle3d"""
    def __init__(self):
        """ Aquest es el mètode inicialitzador de la clase, on la tortuga inicia a l'origen de coordenades, mirant cap a la dreta i amb color roig"""
        self.color = vector(1, 0, 0)
        self.pos = vector(0, 0, 0)
        self.hor = 90
        self.ver = 0
        self.pintar = True
        scene.height = scene.width = 1000
        scene.autocenter = True
        scene.caption = """\nTo rotate "camera", drag with right button or Ctrl-drag.\nTo zoom, drag with middle button or Alt/Option depressed, or use scroll wheel.\n  On a two-button mouse, middle is left + right.\nTo pan left/right and up/down, Shift-drag.\nTouch screen: pinch/extend to zoom, swipe or two-finger rotate.\n"""

    def color(self, x, y, z):
        """ Aquest metode serveix per definir el color amb el que es pintarà"""
        self.color = vector(x, y, z)

    def forward(self, k):
        """ Aquest mètode serveix per moure la tortuga endavant k cops en la direccio cap on mira"""
        ini = self.pos
        x = k * sin(radians(self.hor)) * cos(radians(self.ver))
        y = k * sin(radians(self.ver))
        z = k * cos(radians(self.hor)) * cos(radians(self.ver))
        self.pos += vector(x, y, z)
        if self.pintar:
            cylinder(pos=ini, axis=vector(x, y, z), radius=0.1, color=self.color)
            sphere(pos=ini, radius=0.1, color=self.color)
            sphere(pos=self.pos, radius=0.1, color=self.color)

    def backward(self, k):
        """ Aquest mètode serveix per fer retrocedir la tortuga k cops en la direccio cap on mira"""
        ini = self.pos
        x = k * sin(radians(self.hor)) * cos(radians(self.ver)) * (-1)
        y = k * sin(radians(self.ver)) * (-1)
        z = k * cos(radians(self.hor)) * cos(radians(self.ver)) * (-1)
        self.pos += vector(x, y, z)
        if self.pintar:
            cylinder(pos=ini, axis=vector(x, y, z), radius=0.1, color=self.color)
            sphere(pos=ini, radius=0.1, color=self.color)
            sphere(pos=self.pos, radius=0.1, color=self.color)

    def right(self, a):
        """ Aquest mètode serveix per fer girar cap a l'esquerra a la tortuga un cert angle a"""
        self.hor = (self.hor - a)
        if self.hor < 0:
            self.hor += 360

    def left(self, a):
        """ Aquest mètode serveix per fer girar cap a la dreta a la tortuga un cert angle a"""
        self.hor = (self.hor + a) % 360

    def down(self, a):
        """ Aquest mètode serveix per fer girar cap amunt a la tortuga un cert angle a"""
        self.ver = (self.ver - a)
        if self.ver < 0:
            self.ver += 360

    def up(self, a):
        """ Aquest mètode serveix per fer girar cap avall a la tortuga un cert angle a"""
        self.ver = (self.ver + a) % 360

    def show(self):
        """ Aquest mètode serveix per fer que la tortuga pinti quan es mou"""
        self.pintar = True

    def hide(self):
        """ Aquest mètode serveix per fer que la tortuga deixi de pintar quan es mou"""
        self.pintar = False

    def home(self):
        """ Aquest mètode serveix per retornar la tortuga a la posició original"""
        self.pos = vector(0, 0, 0)
