import pygame


# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # sub-classes must override
        pass

    def update(self, dt):
        # sub-classes must override
        pass

    def circle_circle_collision(self, CircleShape):
        if (
            self.position.distance_to(CircleShape.position)
            <= self.radius + CircleShape.radius
        ):
            return True
        return False

    def circle_triangle_point_collision(self, CircleShape):
        points = CircleShape.triangle()
        if (
            self.position.distance_to(points[0]) <= self.radius
            or self.position.distance_to(points[1]) <= self.radius
            or self.position.distance_to(points[2]) <= self.radius
        ):
            return True

        return False

    def circle_triangle_edge_collision(self, CircleShape):
        points = CircleShape.triangle()
        edges = [(points[0], points[1]), (points[1], points[2]), (points[2], points[0])]

        for edge_start, edge_end in edges:
            edge_vec = edge_end - edge_start
            distance_to_circle = self.position - edge_start

            edge_length_sq = edge_vec.length_squared()

            t = max(0, min(1, edge_vec.dot(distance_to_circle) / edge_length_sq))
            closest_point = edge_start + edge_vec * t

            if self.position.distance_to(closest_point) <= self.radius:
                return True

        return False

    def collided(self, CircleShape):
        if hasattr(CircleShape, "triangle"):
            return self.circle_triangle_point_collision(
                CircleShape
            ) or self.circle_triangle_edge_collision(CircleShape)
        else:
            return self.circle_circle_collision(CircleShape)
