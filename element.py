import pygame
from constants import *


class Element:
    def __init__(
       self,
       size: tuple[int, int],
       pos: tuple[int, int]):  # Position of the centre

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
       text: str = "",
       text_style: str = "",
       text_offset: tuple[int, int] = (0, 0),
       font_face: str = FONT_FACE,
       text_color: tuple[int, int, int] = BLACK,
       color: tuple[int, int, int] = WHITE,
       hovered_color: tuple[int, int, int] = None,
       clicked_color: tuple[int, int, int] = None,
       curve: int = 0
    ):
        super().__init__(size, pos)

        self.func = function

        text_style = text_style.split()
        b_font = pygame.font.SysFont(font_face, self.height - self.height//4)
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
        self._c = color
        self._hc = hovered_color
        self._cc = clicked_color
        
        self._curve = curve

    @property
    def hovered(self):
        mousex = pygame.mouse.get_pos()[0]
        mousey = pygame.mouse.get_pos()[1]

        return self.L<mousex<self.R and self.U<mousey<self.D

    @property
    def clicked(self):
        return self.hovered and pygame.mouse.get_pressed(3)[0]

    def render(self, surface):
        if   self.clicked: color = self._cc
        elif self.hovered: color = self._hc
        else:              color = self._c

        angle1 = (self.LU[0]+self._curve + 1, self.LU[1]+self._curve + 1)
        angle2 = (self.RU[0]-self._curve, self.RU[1]+self._curve + 1)
        angle3 = (self.RD[0]-self._curve, self.RD[1]-self._curve)
        angle4 = (self.LD[0]+self._curve + 1, self.LD[1]-self._curve)

        points = (
            (self.LU[0], self.LU[1] + self._curve + 1),
            (self.LU[0] + self._curve + 1, self.LU[1]),
            (self.RU[0] - self._curve, self.RU[1]),
            (self.RU[0], self.RU[1] + self._curve + 1),
            (self.RD[0], self.RD[1] - self._curve),
            (self.RD[0] - self._curve, self.RD[1]),
            (self.LD[0] + self._curve + 1, self.LD[1]),
            (self.LD[0], self.LD[1] - self._curve)
        )
        text_pos = (
            self.x - self._text.get_width()//2 + self._text_offset[0],
            self.y - self._text.get_height()//2 + self._text_offset[1]
        )

        # Main body
        pygame.draw.polygon(surface, color, points)
        
        # Rounds edges
        pygame.draw.circle(surface, color,angle1, self._curve)
        pygame.draw.circle(surface, color,angle2, self._curve)
        pygame.draw.circle(surface, color,angle3, self._curve)
        pygame.draw.circle(surface, color,angle4, self._curve)

        # Adds text
        surface.blit(self._text, text_pos)


class Label(Element):
    def __init__(
       self,
       text: str,
       pos: tuple[int, int],
       text_color: tuple[int, int, int],
       text_style: str,
       font_size: int,
       font_face: str,
       tilt: float):

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

        super().__init__((self.width, self.height), pos)

    def render(self, surface):
        surface.blit(self._text, self.pos)
