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

        self._flipped_x = False
        self._flipped_y = inv_grav

        self._inv_grav = inv_grav

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

    def flip_x(self, flip):
        if self._flipped_x == flip:
            return
        self.image = pygame.transform.flip(self.image, True, False)
        for i in range(len(self._anim)):
            self._anim[i] = pygame.transform.flip(self._anim[i], True, False)
        self._flipped_x = flip

    def flip_y(self, flip):
        if self._flipped_y == flip:
            return
        self.image = pygame.transform.flip(self.image, False, True)
        for i in range(len(self._anim)):
            self._anim[i] = pygame.transform.flip(self._anim[i], False, True)
        self._flipped_y = flip

    def move(self, t):
        invgrav = -1 if self._inv_grav else 1
        is_grav_inv = global_variables.gravity > 0
        inv = invgrav if global_variables.gravity > 0 else -invgrav
        inv_flip = invgrav + 1 and is_grav_inv or invgrav - 1 and not is_grav_inv
        self.flip_y(not inv_flip)

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            self.x_speed /= DECELERATION
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x_speed = SPEED * inv * t
            self.flip_x(not inv_flip)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x_speed = -SPEED * inv * t
            self.flip_x(inv_flip)
        else:
            self.x_speed /= DECELERATION

        self.y_speed += global_variables.gravity * invgrav
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.can_jump:
            self.y_speed = -JUMP_HEIGHT * inv
            self.can_jump = False
            pygame.mixer.Sound.play(jump)
        if abs(self.y_speed) > self.rect.height:
            self.y_speed = self.rect.height if self.y_speed > 0 else -self.rect.height

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
            # inv - i == not inv + 1
            if self.y_speed < 0 and inv - 1 or\
               self.y_speed > 0 and inv + 1:
                self.can_jump = True

            # Prevents the game from freezing
            for _ in range(1000):
                if self.collisions == 0:
                    break
                self.y += self.y_speed * -.1
            self.y_speed = 0


    def render(self, surface, time_elapsed):
        self.move(time_elapsed)
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
        animation_images=["images/walk_1.png", "images/walk_2.png", "images/walk_1.png", "images/walk_2.png"],
        hitbox="auto",
        pos=(550, 974),
        scale=(38, 44),
        inv_grav=False,
        level=levels[global_variables.current_level][0]
    )

player2 = Player(
        base_image="images/astronaut.png",
        animation_images=["images/walk_1.png", "images/walk_2.png", "images/walk_1.png", "images/walk_2.png"],
        hitbox="auto",
        pos=(1350, 780),
        scale=(38, 44),
        inv_grav=True,
        level=levels[global_variables.current_level][1]
    )
