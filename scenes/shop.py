import random
from cards.cards import Card, get_card_names, generate_card

SHOP_SIZE = (900, 720)


class Shop:
    def __init__(self):
        cards_on_sale = []
        for _ in range(5):
            # For now, just 5 random cards from the general pool.
            cards_on_sale.append(random.choice(get_card_names()))
        self.cards_on_sale: list[Card] = [generate_card(name) for name in cards_on_sale]

    def render(self):
        # Returns shop surface that you can blit onto a screen.
        pass
