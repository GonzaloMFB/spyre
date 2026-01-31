import csv
import os
from copy import deepcopy
import pygame as pg

DIR = os.path.dirname(os.path.abspath(__file__))

CARD_KEYWORDS = [
    "exhaust",
    "retain",
    "innate",
    "ethereal",
    "unplayable",
]


class Card:
    def __init__(
        self,
        name: str,
        card_type: str,
        color: str,
        rarity: str,
        cost: int,
        functions: list,
        base_values: list,
        keywords: list,
        description: str,
    ):
        self.name = name
        self.card_type = card_type
        self.color = color
        self.rarity = rarity
        self.cost = cost
        self.functions = functions
        self.base_values = base_values
        if not keywords:
            self.keywords = []
        elif all([keyword in CARD_KEYWORDS for keyword in keywords]):
            self.keywords = keywords
        else:
            self.keywords = []
            print(f"ERROR - Card keyword list {keywords} contains illegal keyword.")
        self.description = description

    def generate_description(self):
        return self.description.format(*self.base_values)

    def _render_card_text(self, image: pg.surface.Surface):
        # Cost
        cost_txt = pg.font.SysFont("arial", 18).render(str(self.cost), True, (0, 0, 0))
        image.blit(cost_txt, (20, 14))
        # Name
        name_txt = pg.font.SysFont("arial", 18).render(str(self.name), True, (0, 0, 0))
        image.blit(name_txt, (64, 30))
        # Type
        type_txt = pg.font.SysFont("arial", 18).render(str(self.name), True, (0, 0, 0))
        image.blit(type_txt, (90, 135))
        # Description
        desc_txt = self.generate_description()
        type_txt = pg.font.SysFont("arial", 18).render(desc_txt, True, (0, 0, 0))
        image.blit(type_txt, (50, 180))
        return image

    def render_card(self):
        bg = pg.image.load(os.path.join(DIR, "../assets/placeholder_card.png"))
        bg = bg.convert()
        bg.set_colorkey((255, 255, 255))
        # Render blit image text on top of the surface.
        bg = self._render_card_text(bg)
        return bg


def load_card_data():
    """
    Loads card data in memory
    """
    data = {}
    cards_path = os.path.join(DIR, "cards.csv")
    with open(cards_path, "r", newline="\n") as reader:
        fieldnames = next(reader).strip().split("|")
        card_data = csv.DictReader(reader, fieldnames=fieldnames, delimiter="|")
        for card in card_data:
            name = card.pop("name")
            card["base_values"] = card["base_values"].split(",")
            card["functions"] = card["functions"].split(",")
            if card["keywords"]:
                card["keywords"] = card["keywords"].split(",")
            else:
                card["keywords"] = []
            data[name] = card
    return data


card_data = load_card_data()


def generate_card(name: str):
    """
    Docstring for generate_card

    :param name: Card name, which is used to get the template from card_data
    """
    if name not in card_data:
        raise ValueError(f"Unknown card: {name}")
    print(f"Generating {name.title()} card.")

    template = card_data[name]
    instance_data = deepcopy(template)
    return Card(name=name, **instance_data)
