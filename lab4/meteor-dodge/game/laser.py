import pygame


class Laser:
    SPEED = 11

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = 16
        self.radius = 4
        self.color = (120, 255, 180)

    def update(self):
        self.y -= self.SPEED

    def off_screen(self):
        return self.y + self.length < 0

    def hits(self, meteor):
        dx = self.x - meteor.x
        dy = self.y - meteor.y
        return (dx ** 2 + dy ** 2) ** 0.5 < meteor.radius + self.radius

    def draw(self, screen):
        pygame.draw.line(screen, self.color,
                         (int(self.x), int(self.y)),
                         (int(self.x), int(self.y + self.length)), 3)
        pygame.draw.circle(screen, (210, 255, 230), (int(self.x), int(self.y)), 2)
