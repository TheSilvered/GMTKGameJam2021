import pygame
import os

pygame.init()


class Element:
    """This is the basic instance of every object in the scene.
    
    pos: position of the upper left corner
    c_pos: position of the centre,
    size: size of the element [width, height]
    c_size: size to scale from the centre [width, height]
    texture: the part to blit on the surface when calling render
    parent: another element where you can anchor this instance of element
    anchor: where the upper left corner of the element should be relative
            to it's parent. Accepted values: _lu, _ld, _ru, _rd, _cu, _cd
            _cl, _cr, _c
    c_anchor: where the centre of the element should be relative
            to it's parent. Accepted values: _lu, _ld, _ru, _rd, _cu, _cd
            _cl, _cr, _c
    """

    def __init__(self,
       pos: tuple[int, int] = None,
       c_pos: tuple[int, int] = None,
       size: tuple[int, int] = None,
       c_size: tuple[int, int] = None,
       texture: pygame.Surface = None,
       parent=None,
       anchor: str = "",
       c_anchor: str = "",
       offset: (tuple[int, int], int) = None,
       visible: bool = True):
        
        if parent is None and (anchor != "" or c_anchor != ""):
            raise TypeError("element anchored without parent")

        if pos is None and c_pos is None and parent is None:
            raise TypeError("__init__ missing one positional argument ('pos', 'c_pos' or 'parent'+'anchor')")

        # Size should default to (0, 0) if it's not defined
        if size is None and c_size is None:
            size = (0, 0)

        if size is not None:
            self._size = size
        else:
            self._size = (c_size[0] * 2, c_size[1] * 2)
        self._width = self._size[0]
        self._height = self._size[1]

        self._anc = False
        self._c_anc = False
        self._anc_type = ""
        self._anc_offset = offset if offset is not None else (0, 0)
        self._p = parent
        if pos is not None:
            self._pos = pos
        elif c_pos is not None:
            self._pos = (c_pos[0] - self._width/2, c_pos[1] - self._height/2)
        elif anchor != "":
            self._pos = None
            self._anc = True
            self._anc_type = anchor
        elif c_anchor != "":
            self._pos = None
            self._c_anc = True
            self._anc_type = c_anchor

        if texture is None:
            texture = pygame.Surface((2, 2))
            texture.set_at((0, 0), (255, 0, 255))
            texture.set_at((1, 1), (255, 0, 255))

        self._texture = pygame.transform.scale(texture, self._size)
        self.visible = visible

    @property
    def x(self):
        return self.pos[0]
    @x.setter
    def x(self, value):
        self.pos = (value, self.pos[1])

    @property
    def y(self):
        return self.pos[1]
    @y.setter
    def y(self, value):
        self.pos = (self.pos[0], value)

    @property
    def pos(self):
        if self._pos is not None:
            return self._pos
        elif self._anc:
            pos = list(getattr(self._p, self._anc_type))
            pos[0] += self._anc_offset[0]
            pos[1] += self._anc_offset[1]
            return tuple(pos)
        else:
            c_pos = list(getattr(self._p, self._anc_type))
            c_pos[0] = c_pos[0] - self._width/2 + self._anc_offset[0]
            c_pos[1] = c_pos[1] - self._height/2 + self._anc_offset[1]
            return tuple(c_pos)

    @pos.setter
    def pos(self, value):
        if self._anc or self._c_anc:
            raise NotImplementedError("cannot set the position of an anchored element")
        self._pos = value

    @property
    def _l(self): return self.pos[0]
    @property
    def _u(self): return self.pos[1]
    @property
    def _r(self): return self.pos[0] + self._width
    @property
    def _d(self): return self.pos[1] + self._height
    @property
    def _c(self): return (self._l + self._width/2, self._u + self._height/2)
    @property
    def _lu(self): return (self._l, self._u)
    @property
    def _ld(self): return (self._l, self._d)
    @property
    def _ru(self): return (self._r, self._u)
    @property
    def _rd(self): return (self._r, self._d)
    @property
    def _cu(self): return (self._c[0], self._u)
    @property
    def _cd(self): return (self._c[0], self._d)
    @property
    def _cl(self): return (self._l, self._c[1])
    @property
    def _cr(self): return (self._r, self._c[1])

    def render(self, surface):
        if self.visible:    
            surface.blit(self._texture, self.pos)
