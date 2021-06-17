import pygame
from .element import Element
from .label import Label
from PIL import Image, ImageFilter

pygame.init()


def blur(surface, size):
    w = surface.get_width()
    h = surface.get_height()
    ns = pygame.Surface((w, h))
    ns.convert_alpha()
    # print(colors)
    for i in range(w):
        for j in range(h):
            avrage = [0, 0, 0, 0]
            div_count = 0
            for y in range(-size, size + 1):
                for x in range(-size, size + 1):
                    if -size <= x + y <= size + 1:
                        try:
                            col = surface.get_at((j-x, i-y))
                            avrage[0] += col[0]
                            avrage[1] += col[1]
                            avrage[2] += col[2]
                            avrage[3] += col[3]
                            div_count += 1
                        except IndexError:
                            pass
            if div_count != 0:
                avrage[0] //= div_count
                avrage[1] //= div_count
                avrage[2] //= div_count
                avrage[3] //= (size + 1) ** 4
                ns.set_at((j, i), avrage)
    ns.convert_alpha()
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
        texture_size = (self._width + halo*2, self._height + halo*2)
        texture = pygame.Surface(texture_size, pygame.SRCALPHA)
        if color == (0, 0, 0):
            main_body.set_colorkey((255, 255, 255))
            texture.set_colorkey((255, 255, 255))
        else:
            main_body.set_colorkey((0, 0, 0))
            texture.set_colorkey((0, 0, 0))
        texture.convert_alpha()
        main_body.convert_alpha()

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
            for i in range(texture_size[0]):
                alphas.append([])
                for j in range(texture_size[1]):
                    alphas[i].append(texture.get_at((i, j))[3])

            texture_str = pygame.image.tostring(texture, "RGBA")
            blured_halo = Image.frombytes("RGBA", texture_size, texture_str)
            blured_halo = blured_halo.filter(ImageFilter.GaussianBlur(radius=6))
            blured_halo_str = blured_halo.tobytes()
            texture = pygame.image.fromstring(blured_halo_str, texture_size, "RGBA")

            for i in range(texture_size[0]):
                for j in range(texture_size[1]):
                    r, g, b, _ = texture.get_at((i, j))
                    a = alphas[i][j]
                    texture.set_at((i, j), (r, g, b, a))

        main_body.set_alpha(255)
        texture.blit(main_body, (halo, halo))
        text_kwargs["c_pos"] = (texture.get_width()/2, texture.get_height()/2)
        text = Label(**text_kwargs)
        text.x += text._anc_offset[0]
        text.y += text._anc_offset[1]
        text.render(texture)
        texture.convert_alpha()
        return texture

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
