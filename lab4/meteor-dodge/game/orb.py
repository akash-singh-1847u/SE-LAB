import pygame
import random
import math


class Orb:
    # Task 3: a drifting energy orb that grants a temporary shield when collected.
    def __init__(self, width):
        self.x = random.randint(40, width - 40)
        self.y = -20
        self.radius = 11
        self.vx = random.uniform(-1.0, 1.0)
        self.vy = random.uniform(1.2, 2.2)
        self.phase = random.uniform(0, math.pi * 2)
        self.color = (90, 220, 255)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.phase += 0.15

    def off_screen(self, height):
        return self.y > height + 30

    def collected_by(self, rect):
        dx = self.x - rect.centerx
        dy = self.y - rect.centery
        return (dx ** 2 + dy ** 2) ** 0.5 < self.radius + 18

    def draw(self, screen):
        pulse = 2 + int(2 * math.sin(self.phase))
        glow = pygame.Surface((70, 70), pygame.SRCALPHA)
        pygame.draw.circle(glow, (90, 220, 255, 55), (35, 35), self.radius + pulse + 8)
        screen.blit(glow, (int(self.x - 35), int(self.y - 35)))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius + pulse)
        pygame.draw.circle(screen, (235, 255, 255), (int(self.x), int(self.y)), max(2, self.radius // 2))
