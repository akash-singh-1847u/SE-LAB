import pygame
import random
import math


class Meteor:
    # Meteors at or above this radius are "large" and split when destroyed.
    LARGE_THRESHOLD = 20

    def __init__(self, width, x=None, y=None, radius=None, vx=None, vy=None):
        self.x = x if x is not None else random.randint(0, width)
        self.y = y if y is not None else -30
        self.radius = radius if radius is not None else random.randint(12, 28)

        if vx is None or vy is None:
            angle = random.uniform(70, 110)
            speed = random.uniform(2, 5)
            self.vx = math.cos(math.radians(angle)) * speed
            self.vy = math.sin(math.radians(angle)) * speed
        else:
            self.vx = vx
            self.vy = vy

        self.color = (
            random.randint(160, 220),
            random.randint(80, 120),
            random.randint(40, 80),
        )
        self.rot = 0
        self.rot_speed = random.uniform(-3, 3)

    def is_large(self):
        return self.radius >= self.LARGE_THRESHOLD

    def split(self, width):
        # Task 2: a large meteor fractures into smaller fragments that diverge
        # outwards; a small meteor returns nothing and so dissolves entirely.
        if not self.is_large():
            return []
        children = []
        count = random.randint(2, 3)
        child_radius = max(8, self.radius // 2)
        base = random.uniform(0, 360)
        for i in range(count):
            angle = base + (360 / count) * i + random.uniform(-15, 15)
            speed = random.uniform(2.5, 4.5)
            cvx = math.cos(math.radians(angle)) * speed
            cvy = abs(math.sin(math.radians(angle)) * speed) + 1.0  # keep them falling
            children.append(
                Meteor(width, x=self.x, y=self.y, radius=child_radius, vx=cvx, vy=cvy)
            )
        return children

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rot = (self.rot + self.rot_speed) % 360

    def off_screen(self, height):
        return self.y > height + 60

    def collides(self, rect):
        cx, cy = rect.centerx, rect.centery
        dx, dy = self.x - cx, self.y - cy
        return (dx ** 2 + dy ** 2) ** 0.5 < self.radius + 16

    def draw(self, screen):
        pts = []
        for i in range(7):
            angle = math.radians(self.rot + i * (360 / 7))
            r = self.radius * (0.8 + 0.2 * (i % 2))
            pts.append((int(self.x + r * math.cos(angle)), int(self.y + r * math.sin(angle))))
        pygame.draw.polygon(screen, self.color, pts)
        inner = [(int(self.x + (r * 0.5) * math.cos(math.radians(self.rot + i * (360 / 7)))),
                  int(self.y + (r * 0.5) * math.sin(math.radians(self.rot + i * (360 / 7)))))
                 for i, (cx, cy) in enumerate(pts)]
        pygame.draw.polygon(screen, tuple(max(0, c - 40) for c in self.color), inner)
