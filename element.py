import pygame
from constants import *


class Element:
    def __init__(
       self,
       size: tuple[int, int],
       pos: tuple[int, int],
       visible: bool = True):  # Position of the centre

        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

        self.L = pos[0] - size[0]//2
        self.R = pos[0] + size[0]//2
        self.U = pos[1] - size[1]//2
        self.D = pos[1] + size[1]//2

        self.LU = (self.L, self.U)
        self.CU = (self.x, self.U)
        self.RU = (self.R, self.U)
        self.LC = (self.L, self.y)
        self.CC = (self.x, self.y)
        self.RC = (self.R, self.y)
        self.LD = (self.L, self.D)
        self.CD = (self.x, self.D)
        self.RD = (self.R, self.D)

        self.size = size
        self.width = size[0]
        self.height = size[1]

        self.visible = visible


class Image(Element):
    def __init__(
       self,
       pos: tuple[int, int],
       path: str):  # Position of the centre
        pass


class Button(Element):
    def __init__(
       self,
       pos: tuple[int, int],  # Position of the centre
       function: str,
       size: tuple[int, int],
       args: list = None,
       kwargs: dict = None,
       text: str = "",
       text_style: str = "",
       text_offset: tuple[int, int] = (0, 0),
       font_face: str = FONT_FACE,
       text_color: tuple[int, int, int] = BLACK,
       color: tuple[int, int, int] = WHITE,
       bg_color: tuple[int, int, int] = BG_COLOR,
       hovered_color: tuple[int, int, int] = None,
       clicked_color: tuple[int, int, int] = None,
       curve: int = 0,
       halo: int = 0,  # Is automatically set to be even
       visible: bool = True
    ):
        super().__init__(size, pos, visible)

        if args is None:
            args = []
        if kwargs is None:
            kwargs = {}
        self.func = function
        self._args = args
        self._kwargs = kwargs

        text_style = text_style.split()
        font_size = self.height - self.height//4
        b_font = pygame.font.SysFont(font_face, font_size)
        if "bold" in text_style:
            b_font.set_bold(True)
        if "italic" in text_style:
            b_font.set_italic(True)
        if "underline" in text_style:
            b_font.set_underline(True)
        self._text = b_font.render(text, True, text_color)
        self._text_offset = text_offset

        if hovered_color is None:
            hovered_color = color
        if clicked_color is None:
            clicked_color = hovered_color
        self._c  = color
        self._hc = hovered_color
        self._cc = clicked_color
        self._bg = bg_color
        
        if halo % 2: halo -= 1
        self._halo = halo
        self._curve = curve

    @property
    def hovered(self):
        mousex = pygame.mouse.get_pos()[0]
        mousey = pygame.mouse.get_pos()[1]

        return self.L < mousex < self.R and self.U < mousey < self.D

    @property
    def clicked(self):
        return self.hovered and pygame.mouse.get_pressed(3)[0]

    def render(self, surface):
        if not self.visible:
            return

        if   self.clicked: color = self._cc
        elif self.hovered: color = self._hc
        else:              color = self._c

        if self.hovered:
            halo = int(self._halo * 1.5)
        else:
            halo = self._halo

        button_surface = pygame.Surface(self.size)
        button_surface.fill(self._bg)

        # Without the "+ 1"s the curves would not be consistent
        angle1 = (             self._curve + 1, self._curve + 1          )
        angle2 = (self.width - self._curve    , self._curve + 1          )
        angle3 = (self.width - self._curve    , self.height - self._curve)
        angle4 = (             self._curve + 1, self.height - self._curve)

        points = (
            (0                           ,               self._curve + 1),
            (             self._curve + 1, 0                            ),
            (self.width - self._curve    , 0                            ),
            (self.width                  ,               self._curve + 1),
            (self.width                  , self.height - self._curve    ),
            (self.width - self._curve    , self.height                  ),
            (             self._curve + 1, self.height                  ),
            (0                           , self.height - self._curve    )
        )
        text_pos = (
            self.x - self._text.get_width()//2  + self._text_offset[0],
            self.y - self._text.get_height()//2 + self._text_offset[1]
        )

        # Main body
        pygame.draw.polygon(button_surface, color, points)
        
        # Rounds edges
        pygame.draw.circle(button_surface, color,angle1, self._curve)
        pygame.draw.circle(button_surface, color,angle2, self._curve)
        pygame.draw.circle(button_surface, color,angle3, self._curve)
        pygame.draw.circle(button_surface, color,angle4, self._curve)

        surface.blit(button_surface, self.LU)

        if self._halo > 0:
            alpha = 0 + 255//halo
            button_surface.set_alpha(alpha)
            for i in range(0, halo, 2):
                new_size = (self.width + i, self.height + i)
                new_pos = (self.L - i//2, self.U - i//2)
                new_bs = pygame.transform.scale(button_surface, new_size)
                surface.blit(new_bs, new_pos)
                alpha += alpha

        # Adds text now
        # The text should not be affected by the halo
        surface.blit(self._text, text_pos)

    def execute(self):
        if not self.visible:
            return

        self.func(*self._args, **self._kwargs)


class Label(Element):
    def __init__(
       self,
       pos: tuple[int, int],
       text: str,
       font_size: int,
       text_color: tuple[int, int, int] = BLACK,
       text_style: str = "",
       font_face: str = FONT_FACE,
       tilt: float = 0,
       visible: bool = True):

        text_style = text_style.split()
        b_font = pygame.font.SysFont(font_face, font_size)
        if "bold" in text_style:
            b_font.set_bold(True)
        if "italic" in text_style:
            b_font.set_italic(True)
        if "underline" in text_style:
            b_font.set_underline(True)

        self._text = b_font.render(text, True, text_color)
        self._text = pygame.transform.rotate(self._text, tilt)

        self.width = self._text.get_width()
        self.height = self._text.get_height()

        pos = (
            pos[0] - self.width / 2,
            pos[1] - self.height / 2
        )

        super().__init__((self.width, self.height), pos, visible)

    def render(self, surface):
        surface.blit(self._text, self.pos)
