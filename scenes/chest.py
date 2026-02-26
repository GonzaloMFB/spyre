import os

import pygame

DIR = os.path.dirname(os.path.abspath(__file__))


class Chest:
    def __init__(self):
        self.continue_button = pygame.image.load(
            os.path.join(DIR, "../assets/placeholder_continue.png")
        )
        self.chest_icon = pygame.image.load(
            os.path.join(DIR, "../assets/placeholder_chest.png")
        )
        self.cont_coords = None
        self.open = False

    def is_continue_clicked(self, mouse_pos):
        if not self.cont_coords:
            print("No coords set")
            return False
        in_x = (
            self.cont_coords[0]
            <= mouse_pos[0]
            <= self.cont_coords[0] + self.continue_button.get_width()
        )
        in_y = (
            self.cont_coords[1]
            <= mouse_pos[1]
            <= self.cont_coords[1] + self.continue_button.get_height()
        )
        if in_x and in_y:
            print("Clicked continue box!")
            return True
        return False

    def render(self, screen):
        # For chests, the option to continue and skip it is always present.
        self.cont_coords = (
            screen.get_width() - self.continue_button.get_width(),
            screen.get_height() // 2,
        )
        screen.blit(self.continue_button, self.cont_coords)
