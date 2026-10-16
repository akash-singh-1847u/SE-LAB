import pygame
import random
from game.ship import Ship
from game.meteor import Meteor
from game.laser import Laser
from game.orb import Orb

WIDTH, HEIGHT = 700, 520
FPS = 60
BG = (8, 5, 20)

SHIELD_DURATION = 8 * FPS       # how long a collected shield lasts
ORB_SPAWN_INTERVAL = 9 * FPS    # frames between power-up orb spawns
MULTIPLIER_STEP = 10 * FPS      # survive this long without a hit -> +1x


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Meteor Dodge")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20, bold=True)
        self.small_font = pygame.font.SysFont("monospace", 18, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 46, bold=True)
        self.stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3))
                      for _ in range(80)]
        self.reset()

    def reset(self):
        self.ship = Ship(WIDTH // 2, HEIGHT - 80)
        self.meteors = []
        self.lasers = []
        self.orbs = []
        self.timer = 0
        self.spawn_interval = 60
        self.orb_timer = 0
        self.frames = 0          # total frames survived (drives the time display)
        self.score = 0.0         # accumulated points
        self.streak = 0          # frames since the last hit (drives the multiplier)
        self.multiplier = 1
        self.shield_timer = 0    # frames of shield left, 0 means unshielded
        self.game_over = False
        self.started = False

    def fire_laser(self):
        self.lasers.append(Laser(self.ship.rect.centerx, self.ship.rect.top))

    def register_hit(self):
        # Ship touched a meteor. With a shield up, absorb the hit and reset the
        # streak (Task 3 + Task 4); otherwise the run ends.
        if self.shield_timer > 0:
            self.shield_timer = 0
            self.ship.shielded = False
            self.streak = 0
            self.multiplier = 1
        else:
            self.game_over = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset()
                    elif not self.started:
                        self.started = True
                    else:
                        self.fire_laser()   # Task 1: SPACE fires during flight
        return True

    def update(self):
        if self.game_over or not self.started:
            return

        keys = pygame.key.get_pressed()
        self.ship.move(keys, WIDTH, HEIGHT)
        self.frames += 1

        # Shield countdown (Task 3)
        if self.shield_timer > 0:
            self.shield_timer -= 1
            self.ship.shielded = self.shield_timer > 0

        # Survival multiplier (Task 4): +1x for every 10s without a hit
        self.streak += 1
        self.multiplier = 1 + self.streak // MULTIPLIER_STEP
        self.score += self.multiplier

        # Spawn meteors, with the interval tightening over time
        self.timer += 1
        if self.timer >= self.spawn_interval:
            self.meteors.append(Meteor(WIDTH))
            self.timer = 0
            self.spawn_interval = max(20, self.spawn_interval - 0.3)

        # Spawn orbs (Task 3)
        self.orb_timer += 1
        if self.orb_timer >= ORB_SPAWN_INTERVAL:
            self.orbs.append(Orb(WIDTH))
            self.orb_timer = 0

        # Move projectiles, meteors and orbs
        for l in self.lasers:
            l.update()
        for m in self.meteors:
            m.update()
        for o in self.orbs:
            o.update()

        # Laser vs meteor (Task 1 destroys, Task 2 splits)
        spent_lasers = set()
        destroyed_meteors = set()
        fragments = []
        for li, l in enumerate(self.lasers):
            for mi, m in enumerate(self.meteors):
                if mi in destroyed_meteors:
                    continue
                if l.hits(m):
                    spent_lasers.add(li)
                    destroyed_meteors.add(mi)
                    fragments.extend(m.split(WIDTH))
                    break
        self.lasers = [l for i, l in enumerate(self.lasers)
                       if i not in spent_lasers and not l.off_screen()]
        self.meteors = [m for i, m in enumerate(self.meteors) if i not in destroyed_meteors]
        self.meteors.extend(fragments)

        # Ship vs meteor
        for m in self.meteors:
            if m.collides(self.ship.rect):
                self.register_hit()
                self.meteors.remove(m)
                break

        # Ship vs orb (Task 3)
        remaining = []
        for o in self.orbs:
            if o.collected_by(self.ship.rect):
                self.shield_timer = SHIELD_DURATION
                self.ship.shielded = True
            else:
                remaining.append(o)
        self.orbs = remaining

        # Cull things that have left the screen
        self.meteors = [m for m in self.meteors if not m.off_screen(HEIGHT)]
        self.orbs = [o for o in self.orbs if not o.off_screen(HEIGHT)]

    def draw(self):
        self.screen.fill(BG)
        for sx, sy, sr in self.stars:
            pygame.draw.circle(self.screen, (200, 200, 220), (sx, sy), sr)
        for o in self.orbs:
            o.draw(self.screen)
        for l in self.lasers:
            l.draw(self.screen)
        for m in self.meteors:
            m.draw(self.screen)
        self.ship.draw(self.screen)

        # HUD
        self.screen.blit(self.font.render(f"Time: {self.frames // 60}s", True, (200, 200, 240)), (10, 10))
        self.screen.blit(self.font.render(f"Score: {int(self.score)}", True, (200, 200, 240)), (10, 34))
        self.screen.blit(self.font.render(f"Multiplier: x{self.multiplier}", True, (255, 220, 120)), (10, 58))
        if self.shield_timer > 0:
            self.screen.blit(self.font.render(f"Shield: {self.shield_timer // 60 + 1}s", True, (90, 220, 255)), (10, 82))

        if not self.started:
            msg = self.font.render("Press SPACE to launch", True, (180, 180, 240))
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            hint = self.small_font.render("In flight: SPACE fires lasers, grab orbs for a shield",
                                          True, (140, 140, 200))
            self.screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 30))

        if self.game_over:
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 150))
            self.screen.blit(ov, (0, 0))
            m = self.big_font.render("DESTROYED!", True, (220, 80, 60))
            s = self.small_font.render(
                f"Survived {self.frames // 60}s  |  Score {int(self.score)}  |  SPACE to Restart",
                True, (200, 200, 200))
            self.screen.blit(m, (WIDTH // 2 - m.get_width() // 2, HEIGHT // 2 - 40))
            self.screen.blit(s, (WIDTH // 2 - s.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
