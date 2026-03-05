import os
import pygame

DIR = os.path.dirname(os.path.abspath(__file__))
TOPBAR_SIZE = (1280, 50)
TRANSPARENT = pygame.Color(0, 0, 0, 0)


def load_potion():
    # TODO
    pass


class HealthDisplay:
    def __init__(self, current_health, max_health):
        self.max_health = max_health
        self.current_health = current_health
        self.icon = pygame.image.load(os.path.join(DIR, "../assets/health.png"))
        self.icon = self.icon.convert()
        self.icon.set_colorkey((0, 0, 0))
        self.base_sf = pygame.surface.Surface((100, 40), pygame.SRCALPHA)

    def render(self):
        self.base_sf.fill(TRANSPARENT)
        ft = pygame.font.SysFont("arial", 18)
        text_sf = ft.render(f"{self.current_health}/{self.max_health}", True, (0, 0, 0))
        self.base_sf.blit(self.icon, (0, 0))
        self.base_sf.blit(text_sf, (self.icon.get_width() + 5, 5))
        return self.base_sf


class GoldDisplay:
    def __init__(self, gold):
        self.gold = gold
        self.icon = pygame.image.load(os.path.join(DIR, "../assets/gold.png"))
        self.icon = self.icon.convert()
        self.icon.set_colorkey((0, 0, 0))
        self.base_sf = pygame.surface.Surface((100, 40), pygame.SRCALPHA)

    def render(self):
        self.base_sf.fill(TRANSPARENT)
        ft = pygame.font.SysFont("arial", 18)
        text_sf = ft.render(f"{self.gold}", True, (0, 0, 0))
        self.base_sf.blit(self.icon, (0, 0))
        self.base_sf.blit(text_sf, (self.icon.get_width() + 5, 5))
        return self.base_sf


class PotionDisplay:
    def __init__(self, name=""):
        # Keeps track of potion names to later load imgs.
        if not name:
            self._icon = pygame.image.load(
                os.path.join(DIR, "../assets/placeholder_potion.png")
            )
        else:
            self._icon = load_potion()
        self.icon = self._icon.copy()

    def update_potion(self, name):
        self._icon = load_potion(name)

    def render(self):
        self.icon.fill("white")
        self.icon = self._icon.copy()
        return self.icon


class TopBar:
    def __init__(self, curr_hp, max_hp, gold, max_potions):
        self.origin = (0, 0)
        self.health_ui = HealthDisplay(curr_hp, max_hp)
        self.gold_ui = GoldDisplay(gold)
        self.potions: list[PotionDisplay] = []
        for _ in range(max_potions):
            self.potions.append(PotionDisplay())
        self.layer = 0
        self._window_orig = pygame.image.load(os.path.join(DIR, "../assets/topbar.png"))
        self._window_orig = pygame.transform.scale(self._window_orig, TOPBAR_SIZE)
        self.surface = self._window_orig.copy()

    def update(self, curr_hp, max_hp, gold, layer):
        self.gold_ui.gold = gold
        self.health_ui.max_health = max_hp
        self.health_ui.current_health = curr_hp
        self.layer = layer

    def render(self):
        # Returns surface to blit onto main screen
        # Top bar has five different sections
        self.surface.fill("white")
        self.surface = self._window_orig.copy()
        self.surface.blit(self._render_name(), (50, 15))
        self.surface.blit(self.health_ui.render(), (150, 10))
        self.surface.blit(self.gold_ui.render(), (250, 10))
        self._render_potions((350, 10))
        bg = self._render_layer()
        self.surface.blit(bg, ((self.surface.get_width() - bg.get_width()) // 2, 15))
        return self.surface

    def _render_name(self):
        return pygame.font.SysFont("arial", 18).render("Player", True, (0, 0, 0))

    def _render_potions(self, coords):
        for i, potion in enumerate(self.potions):
            pot_coords = (coords[0] + i * 40, coords[1])
            sf = potion.render()
            self.surface.blit(sf, pot_coords)

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
