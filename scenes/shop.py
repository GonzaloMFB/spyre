import random
import os

import pygame
from cards.cards import Card, get_card_names, generate_card

SHOP_SIZE = (900, 720)
DIR = os.path.dirname(os.path.abspath(__file__))


class Shop:
    def __init__(self):
        self.continue_button = pygame.image.load(
            os.path.join(DIR, "../assets/placeholder_continue.png")
        )
        cards_on_sale = []
        for _ in range(5):
            # For now, just 5 random cards from the general pool.
            cards_on_sale.append(random.choice(get_card_names()))
        self.cards_on_sale: list[Card] = [generate_card(name) for name in cards_on_sale]
        self.open = False
        self.cont_coords = None

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
        # Returns shop surface that you can blit onto a screen.
        if not self.open:
            self.cont_coords = (
                screen.get_width() - self.continue_button.get_width(),
                screen.get_height() // 2,
            )
            screen.blit(self.continue_button, self.cont_coords)
