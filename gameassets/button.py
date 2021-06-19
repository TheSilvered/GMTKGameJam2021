import pygame
from .element import Element
from .label import Label
from PIL import Image, ImageFilter
import json

pygame.init()


def blur(surface, size, color):
    w = surface.get_width()
    h = surface.get_height()
    ns = pygame.Surface((w, h))
    ns.convert_alpha()
    if len(color) > 3:
        color = (color[0], color[1], color[2])

    for i in range(w):
        for j in range(h):
            avrage = 0
            for y in range(-size, size + 1):
                for x in range(-size, size + 1):
                    try:
                        avrage += surface.get_at((j-x, i-y))[3]
                    except IndexError:
                        pass
            avrage //= ((size + 1) * 2) ** 2
            ns.set_at((j, i), color + (avrage,))
    return ns


class Button(Element):
    def __init__(self,
       pos: tuple[int, int] = None,
       c_pos: tuple[int, int] = None,
       size: tuple[int, int] = None,
       c_size: tuple[int, int] = None,
       texture_normal : pygame.Surface = None,
       texture_hovered: pygame.Surface = None,
       texture_clicked: pygame.Surface = None,
       texture_buffers: tuple[bytes, bytes, bytes] = None,
       color_normal : tuple[int, int, int] = None,
       color_hovered: tuple[int, int, int] = None,
       color_clicked: tuple[int, int, int] = None,
       make_texture: bool = True,
       curve: int = 0,
       halo: int = 0,
       halo_intensity: float = 2,
       sound: pygame.mixer.Sound = None,
       text_kwargs: dict = None,
       parent=None,
       anchor: str = "",
       c_anchor: str = "",
       offset: (tuple[int, int], int) = None,
       visible: bool = True,
       window_scale: tuple[int, int] = (1920, 1080),
       function = None,
       args = None,
       kwargs = None):
        super().__init__(pos, c_pos, size, c_size, None, parent, anchor, c_anchor, offset, visible)

        if texture_normal is not None:
            self._tn = texture_normal
            self._th = self._tn if texture_hovered is None else texture_hovered
            self._tc = self._th if texture_clicked is None else texture_clicked
        else:
            color_normal = (0, 0, 0) if color_normal is None else color_normal
            color_hovered = color_normal  if color_hovered is None else color_hovered
            color_clicked = color_hovered if color_clicked is None else color_clicked
            self._cn = color_normal
            self._ch = color_hovered
            self._cc = color_clicked
            self._curve = curve
            self._halo = halo
            self._halo_i = halo_intensity
            if texture_buffers is not None:
                self.buffertexture(*texture_buffers)
            elif make_texture:
                self._tn = self.maketexture(self._cn,     self._halo       , text_kwargs)
                self._th = self.maketexture(self._ch, int(self._halo * 1.5), text_kwargs)
                self._tc = self.maketexture(self._cc, int(self._halo * 1.5), text_kwargs)

            self._render_pos = (self.x - halo, self.y - halo)
            self._render_pos_halo = (self.x - int(halo * 1.5), self.y - int(halo * 1.5))

        self._sound = sound

        self._wscalex = window_scale[0]
        self._wscaley = window_scale[1]

        self._f = function
        self._fargs = [] if args is None else args
        self._fkwargs = {} if kwargs is None else kwargs

    @property
    def hovered(self):
        mousex = (pygame.mouse.get_pos()[0] * 1920) / self._wscalex
        mousey = (pygame.mouse.get_pos()[1] * 1080) / self._wscaley

        return self._l < mousex < self._r and self._u < mousey < self._d

    @property
    def clicked(self):
        return self.hovered and pygame.mouse.get_pressed(3)[0]

    def maketexture(self, color, halo, text_kwargs):
        main_body = pygame.Surface(self._size)
        texture_size = (self._width + halo*2, self._height + halo*2)
        texture = pygame.Surface(texture_size, pygame.SRCALPHA)
        if color == (0, 0, 0):
            main_body.set_colorkey((255, 255, 255))
            texture.set_colorkey((255, 255, 255))
        else:
            main_body.set_colorkey((0, 0, 0))
            texture.set_colorkey((0, 0, 0))
        # texture.convert_alpha()
        # main_body.convert_alpha()

        points = (
            (0                            , self._curve                   ),
            (self._curve                  , 0                             ),
            (self._width - self._curve - 1, 0                             ),
            (self._width - 1              , self._curve                   ),
            (self._width - 1              , self._height - self._curve - 1),
            (self._width - self._curve - 1, self._height - 1              ),
            (self._curve                  , self._height - 1              ),
            (0                            , self._height - self._curve - 1)
        )

        # Without the "+ 1"s the self._curves would not be consistent
        curve1 = (              self._curve + 1,                self._curve + 1)
        curve2 = (self._width - self._curve - 1,                self._curve + 1)
        curve3 = (self._width - self._curve - 1, self._height - self._curve - 1)
        curve4 = (              self._curve + 1, self._height - self._curve - 1)

        pygame.draw.polygon(main_body, color, points)

        pygame.draw.circle(main_body, color, curve1, self._curve)
        pygame.draw.circle(main_body, color, curve2, self._curve)
        pygame.draw.circle(main_body, color, curve3, self._curve)
        pygame.draw.circle(main_body, color, curve4, self._curve)


        if halo > 0 and self._halo_i > 0:
            alpha = 255 / (halo / self._halo_i)
            main_body.set_alpha(alpha)
            for i in range(0, halo, 2):
                main_body.set_alpha(int(alpha))
                new_size = (self._width - i + halo, self._height - i + halo)
                pos = ((i+halo) // 2, (i+halo) // 2)
                new_bs = pygame.transform.scale(main_body, new_size)
                texture.blit(new_bs, pos)
            alphas = []

            w = texture_size[0]//2
            h = texture_size[1]//2
            blurred_texture = pygame.Surface((w, h)).convert_alpha()
            if len(color) > 3:
                color = (color[0], color[1], color[2])

            size = 5

            for i in range(w):
                for j in range(h):
                    avrage = 0
                    for y in range(-size, size + 1):
                        for x in range(-size, size + 1):
                            try:
                                avrage += texture.get_at((i-x, j-y))[3]
                            except IndexError:
                                pass
                    avrage //= ((size + 1) * 2) ** 2
                    blurred_texture.set_at((i, j), color + (avrage,))

            new_texture = pygame.Surface(texture_size, pygame.SRCALPHA)
            new_texture.blit(blurred_texture, (0, 0))
            blurred_texture = pygame.transform.flip(blurred_texture, True, False)
            new_texture.blit(blurred_texture, (w, 0))
            blurred_texture = pygame.transform.flip(blurred_texture, False, True)
            new_texture.blit(blurred_texture, (w, h))
            blurred_texture = pygame.transform.flip(blurred_texture, True, False)
            new_texture.blit(blurred_texture, (0, h))

            texture = new_texture.convert_alpha()

        main_body.set_alpha(255)
        texture.blit(main_body, (halo, halo))
        text_kwargs["c_pos"] = (texture.get_width()/2, texture.get_height()/2)
        text = Label(**text_kwargs)
        text.x += text._anc_offset[0]
        text.y += text._anc_offset[1]
        text.render(texture)
        # print("Done")
        return texture

    def buffertexture(self, tn, th=None, tc=None):
        th_tn = False
        tc_tn = False
        if th is None:
            th = tn
            th_tn = True
        if tc is None:
            tc = th
            if th == tn:
                tc_tn = True

        tn_size = (self._size[0] + self._halo*2, self._size[1] + self._halo*2)
        th_size = (self._size[0] + int(self._halo*1.5) * 2, self._size[1] + int(self._halo*1.5) * 2)
        self._tn = pygame.image.frombuffer(tn, tn_size, "RGBA")
        if th_tn:
            self._th = pygame.image.frombuffer(th, tn_size, "RGBA")
        else:
            self._th = pygame.image.frombuffer(th, th_size, "RGBA")
        if tc_tn:
            self._tc = pygame.image.frombuffer(tc, tn_size, "RGBA")
        else:
            self._tc = pygame.image.frombuffer(tc, th_size, "RGBA")

    def render(self, surface):
        if self.clicked:
            surface.blit(self._tc, self._render_pos_halo)
        elif self.hovered:
            surface.blit(self._th, self._render_pos_halo)
        else:
            surface.blit(self._tn, self._render_pos)

    def run(self):
        if self._f is None:
            return

        if self._sound:
            pygame.mixer.Sound.play(self._sound)

        self._f(*self._fargs, **self._fkwargs)

    def save_textures(self, path):
        tc = pygame.image.tostring(self._tc, "RGBA")
        th = pygame.image.tostring(self._th, "RGBA")
        tn = pygame.image.tostring(self._tn, "RGBA")
        with open(path + "tc.texture", "wb") as f:
            f.write(tc)
        with open(path + "th.texture", "wb") as f:
            f.write(th)
        with open(path + "tn.texture", "wb") as f:
            f.write(tn)
