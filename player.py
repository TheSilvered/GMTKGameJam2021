import pygame

from constants import *
import global_variables
from level import levels

pygame.init()
jump = pygame.mixer.Sound("sounds/jump.wav")
jump.set_volume(0.2)


class Player(pygame.sprite.Sprite):
    def __init__(self, base_image, animation_images, hitbox, pos, scale, inv_grav, level):
        pygame.sprite.Sprite.__init__(self)

        self.x_speed = 0
        self.y_speed = 0

        if isinstance(pos, tuple):
            pos = list(pos)
        self.pos = pos

        self.image = pygame.image.load(base_image)
        self.image = pygame.transform.scale(self.image, scale)
        self._anim = [pygame.transform.scale(pygame.image.load(i), scale) for i in animation_images]
        if inv_grav:
            self.image = pygame.transform.flip(self.image, False, True)
            for i in range(len(self._anim)):
                self._anim[i] = pygame.transform.flip(self._anim[i], False, True)

        self._facing_dir = "right"

        self._grav = -global_variables.gravity if inv_grav else global_variables.gravity
        self._prev_grav = self._grav
        self._starting_grav = self._grav

        if hitbox == "auto":
            hitbox = pygame.Rect(pos, (self.image.get_width(), self.image.get_height()))

        self.rect = hitbox
        self.group = pygame.sprite.Group(self)
        self.level = level

        self.can_jump = True
        self._tick_count = 0

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @x.setter
    def x(self, value):
        self.pos[0] = value
        self.rect.update(value, self.pos[1], self.rect.width, self.rect.height)

    @y.setter
    def y(self, value):
        self.pos[1] = value
        self.rect.update(self.pos[0], value, self.rect.width, self.rect.height)

    @property
    def collisions(self):
        """Returns the number of collisions"""

        collisions = pygame.sprite.groupcollide(
            self.group,
            self.level.blocks,
            False,
            False
        )

        for i in collisions:
            return len(collisions[i])

        return 0

    @property
    def on_door(self):
        collisions = pygame.sprite.groupcollide(
            self.group,
            self.level.door,
            False,
            False
        )
        return len(collisions) > 0

    def set_pos(self, value):
        self.x = value[0]
        self.y = value[1]

    def change_dir(self, dir_):
        if dir_ == self._facing_dir and self._grav < 0:
            self.image = pygame.transform.flip(self.image, True, False)
            for i in range(len(self._anim)):
                self._anim[i] = pygame.transform.flip(self._anim[i], True, False)
            self._facing_dir = "left" if dir_ == "right" else "right"
            
        elif dir_ != self._facing_dir and self._grav > 0:
            self.image = pygame.transform.flip(self.image, True, False)
            for i in range(len(self._anim)):
                self._anim[i] = pygame.transform.flip(self._anim[i], True, False)
            self._facing_dir = dir_

    def move(self):
        if self._starting_grav < 0:
            self._grav = -global_variables.gravity
        else:
            self._grav = global_variables.gravity

        if self._prev_grav != self._grav:
            self.image = pygame.transform.flip(self.image, False, True)
            for i in range(len(self._anim)):
                self._anim[i] = pygame.transform.flip(self._anim[i], False, True)
        self._prev_grav = self._grav

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.x_speed = 0
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x_speed = SPEED * self._grav
            self.change_dir("right")
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x_speed = -SPEED * self._grav
            self.change_dir("left")
        else:
            self.x_speed /= DECELERATION

        self.y_speed += self._grav

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.can_jump:
            self.y_speed = -20 * self._grav / 1.3
            self.can_jump = False
            pygame.mixer.Sound.play(jump)

        self.x += self.x_speed
        if self.collisions > 0:
            # Prevents the game from freezing
            for _ in range(1000):
                if self.collisions == 0:
                    break
                self.x += self.x_speed * -.1
            self.x_speed = 0
        else:
            self.can_jump = False

        self.y += self.y_speed
        if self.collisions > 0:
            if self.y_speed < 0 and self._grav < 0 or\
               self.y_speed > 0 and self._grav > 0:
                self.can_jump = True

            # Prevents the game from freezing
            for _ in range(1000):
                if self.collisions == 0:
                    break
                self.y += self.y_speed * -.1
            self.y_speed = 0


    def render(self, surface):
        self.move()
        self.rect.update(self.pos, (self.rect.width, self.rect.height))
        self._tick_count += 1
        if self._tick_count >= FRAMERATE:
            self._tick_count = 0

        if (0.5 < self.x_speed or -0.5 > self.x_speed) and self.can_jump:
            try:
                surface.blit(self._anim[self._tick_count // (FRAMERATE//len(self._anim))], self.pos)
            except IndexError:
                surface.blit(self._anim[(self._tick_count // (FRAMERATE//len(self._anim))) - 1], self.pos)

            self._tick_count += 1
            if self._tick_count >= FRAMERATE:
                self._tick_count = 0

        else:
            surface.blit(self.image, self.pos)
            self._tick_count = 0


player1 = Player(
        base_image="images/astronaut.png",
        animation_images=["images/walk_1.png", "images/walk_2.png", "images/walk_1.png", "images/walk_2.png",
                          "images/walk_1.png", "images/walk_2.png", "images/walk_1.png", "images/walk_2.png"],
        hitbox="auto",
        pos=(550, 974),
        scale=(38, 44),
        inv_grav=False,
        level=levels[global_variables.current_level][0]
    )

player2 = Player(
        base_image="images/astronaut.png",
        animation_images=["images/walk_1.png", "images/walk_2.png", "images/walk_1.png", "images/walk_2.png",
                          "images/walk_1.png", "images/walk_2.png", "images/walk_1.png", "images/walk_2.png"],
        hitbox="auto",
        pos=(1350, 780),
        scale=(38, 44),
        inv_grav=True,
        level=levels[global_variables.current_level][1]
    )
