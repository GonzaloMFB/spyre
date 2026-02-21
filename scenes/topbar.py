import os
import pygame

DIR = os.path.dirname(os.path.abspath(__file__))
TOPBAR_SIZE = (1280, 50)


class HealthDisplay:
    def __init__(self, current_health, max_health):
        self.max_health = max_health
        self.current_health = current_health
        self.icon = pygame.image.load(
            os.path.join(DIR, "../assets/placeholder_health.png")
        )
        self.icon = self.icon.convert()
        self.icon.set_colorkey((0, 0, 0))
        self.base_sf = pygame.surface.Surface((100, 40))

    def render(self):
        self.base_sf.fill("white")
        ft = pygame.font.SysFont("arial", 18)
        text_sf = ft.render(f"{self.current_health}/{self.max_health}", True, (0, 0, 0))
        self.base_sf.blit(self.icon, (0, 0))
        self.base_sf.blit(text_sf, (self.icon.get_width() + 5, 5))
        return self.base_sf


class GoldDisplay:
    def __init__(self, gold):
        self.gold = gold
        self.icon = pygame.image.load(
            os.path.join(DIR, "../assets/placeholder_gold.png")
        )
        self.icon = self.icon.convert()
        self.icon.set_colorkey((0, 0, 0))
        self.base_sf = pygame.surface.Surface((100, 40))

    def render(self):
        self.base_sf.fill("white")
        ft = pygame.font.SysFont("arial", 18)
        text_sf = ft.render(f"{self.gold}", True, (0, 0, 0))
        self.base_sf.blit(self.icon, (0, 0))
        self.base_sf.blit(text_sf, (self.icon.get_width() + 5, 5))
        return self.base_sf


class PotionsDisplay:
    def __init__(self):
        self.potions = [None, None, None]

    def render(self):
        pass


class TopBar:
    def __init__(self, curr_hp, max_hp, gold):
        self.surface = pygame.surface.Surface(TOPBAR_SIZE)
        self.origin = (0, 0)
        self.health = HealthDisplay(curr_hp, max_hp)
        self.gold = GoldDisplay(gold)
        self.pots = PotionsDisplay()
        self.layer = 0

    def render(self):
        # Returns surface to blit onto main screen
        # Top bar has five different sections
        self.surface.fill("white")
        self.surface.blit(self._render_name(), (50, 15))
        self.surface.blit(self.health.render(), (150, 10))
        self.surface.blit(self.gold.render(), (250, 10))
        # self.surface.blit(self.pots.render(), (250, 15))
        bg = self._render_layer()
        self.surface.blit(bg, ((self.surface.get_width() - bg.get_width()) // 2, 15))
        return self.surface

    def _render_name(self):
        return pygame.font.SysFont("arial", 18).render("Player", True, (0, 0, 0))

    def _render_layer(self):
        return pygame.font.SysFont("arial", 18).render(
            f"Layer {self.layer}", True, (0, 0, 0)
        )


if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    topbar = TopBar(5, 5, 5)
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        screen.fill("gray45")
        screen.blit(topbar.render(), (0, 0))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
