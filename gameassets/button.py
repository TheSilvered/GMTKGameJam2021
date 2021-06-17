import pygame
from .element import Element
from .label import Label

pygame.init()


class Button(Element):
    def __init__(self,
       pos: tuple[int, int] = None,
       c_pos: tuple[int, int] = None,
       size: tuple[int, int] = None,
       c_size: tuple[int, int] = None,
       texture_normal : pygame.Surface = None,
       texture_hovered: pygame.Surface = None,
       texture_clicked: pygame.Surface = None,
       color_normal : tuple[int, int, int] = None,
       color_hovered: tuple[int, int, int] = None,
       color_clicked: tuple[int, int, int] = None,
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
            color_hovered = color_normal  if color_hovered is None else color_hovered
            color_clicked = color_hovered if color_clicked is None else color_clicked
            self._cn = color_normal
            self._ch = color_hovered
            self._cc = color_clicked
            self._curve = curve
            self._halo = halo
            self._halo_i = halo_intensity
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
        texture = pygame.Surface((self._width + halo*2, self._height + halo*2), pygame.SRCALPHA)
        if color == (0, 0, 0):
            main_body.set_colorkey((255, 255, 255))
            texture.set_colorkey((255, 255, 255))
        else:
            main_body.set_colorkey((0, 0, 0))
            texture.set_colorkey((0, 0, 0))
        texture.convert_alpha()
        main_body.convert_alpha()

        points = (
            (0                            ,                self._curve + 1),
            (              self._curve + 1, 0                             ),
            (self._width - self._curve    , 0                             ),
            (self._width                  ,                self._curve + 1),
            (self._width                  , self._height - self._curve    ),
            (self._width - self._curve    , self._height                  ),
            (              self._curve + 1, self._height                  ),
            (0                            , self._height - self._curve    )
        )

        # Without the "+ 1"s the self._curves would not be consistent
        curve1 = (              self._curve + 1,                self._curve + 1)
        curve2 = (self._width - self._curve    ,                self._curve + 1)
        curve3 = (self._width - self._curve    , self._height - self._curve    )
        curve4 = (              self._curve + 1, self._height - self._curve    )

        pygame.draw.polygon(main_body, color, points)

        pygame.draw.circle(main_body, color, curve1, self._curve)
        pygame.draw.circle(main_body, color, curve2, self._curve)
        pygame.draw.circle(main_body, color, curve3, self._curve)
        pygame.draw.circle(main_body, color, curve4, self._curve)

        texture.blit(main_body, (halo, halo))

        if halo > 0 and self._halo_i > 0:
            alpha = 255 / (halo / self._halo_i)
            main_body.set_alpha(alpha)
            for i in range(0, halo, 2):
                main_body.set_alpha(int(alpha))
                new_size = (self._width - i + halo, self._height - i + halo)
                pos = ((i+halo) // 2, (i+halo) // 2)
                new_bs = pygame.transform.scale(main_body, new_size)
                texture.blit(new_bs, pos)

        text_kwargs["c_pos"] = (texture.get_width()/2, texture.get_height()/2)
        text = Label(**text_kwargs)
        text.x += text._anc_offset[0]
        text.y += text._anc_offset[1]
        text.render(texture)
        return texture.convert_alpha()

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
