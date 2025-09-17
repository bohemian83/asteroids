import pygame
from circleshape import CircleShape
from constants import EXPLOSION_LIFETIME


class Explosion(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

        self.lifetime = EXPLOSION_LIFETIME

    def update(self, dt):
        self.lifetime -= dt
        self.radius += 100 * dt  # Expand

        if self.lifetime <= 0:
            self.kill()  # Auto-remove!

    def draw(self, screen):
        if self.radius > 0:
            alpha = max(0, self.lifetime * 5)  # Fade out
            color = (255 * alpha, 200 * alpha, 100 * alpha)
            pygame.draw.circle(screen, color, self.position, int(self.radius), 2)
