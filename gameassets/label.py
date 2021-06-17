import pygame
from .element import Element

pygame.init()


class Label(Element):
    def __init__(self,
       pos: tuple[int, int] = None,
       c_pos: tuple[int, int] = None,
       text: str = "",
       text_size: int = 15,
       text_font:str = "segoeui",
       text_style: str = "",
       color: tuple[int, int, int] = (0, 0, 0),
       tilt: int = 0,
       parent=None,
       anchor: str = "",
       c_anchor: str = "",
       offset: (tuple[int, int], int) = None,
       visible: bool = True):
        
        text_style = text_style.split()
        font = pygame.font.SysFont(text_font, text_size)
        if "bold" in text_style:
            font.set_bold(True)
        if "italic" in text_style:
            font.set_italic(True)
        if "underline" in text_style:
            font.set_underline(True)
        self._font = font
        self._tilt = tilt
        self._color = color
        texture = self._font.render(text, True, self._color)
        texture = pygame.transform.rotate(texture, self._tilt)
        texture.convert_alpha()
        size = (texture.get_width(), texture.get_height())

        super().__init__(pos, c_pos, size, None, texture, parent, anchor, c_anchor, offset, visible)

    def change_text(self, newtxt):
        texture = self._font.render(newtxt, True, self._color)
        texture = pygame.transform.rotate(texture, self._tilt)
        self._texture = texture
        self._size = (texture.get_width(), texture.get_height())
