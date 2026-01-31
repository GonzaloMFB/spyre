import csv
import os
from copy import deepcopy
from entities.entity import Entity


DIR = os.path.dirname(os.path.abspath(__file__))

STARTER_DECKS = {"knight": {"strike": 5, "defend": 4, "bash": 1}}


class Character(Entity):
    def __init__(self, name, color, base_hp):
        super().__init__(base_hp)
        self.name = name
        self.color = color
        self.deck = STARTER_DECKS.get(name, []) or []
        self.max_energy = 3
        self.current_energy = self.max_energy


def load_character_data():
    """
    Loads character data in memory
    """
    data = {}
    char_path = os.path.join(DIR, "characters.csv")
    with open(char_path, "r", newline="\n") as reader:
        fieldnames = next(reader).strip().split("|")
        char_data = csv.DictReader(reader, fieldnames=fieldnames, delimiter="|")
        for char in char_data:
            name = char.pop("name")
            data[name] = char
    return data


char_data = load_character_data()


def generate_char(name: str):
    """
    Character factory.
    :param name: Character name, which is used to get the template from card_data
    """
    if name not in char_data:
        raise ValueError(f"Unknown character: {name}")
    print(f"Generating charater: {name.title()}.")

    template = char_data[name]
    instance_data = deepcopy(template)
    return Character(name=name, **instance_data)


if __name__ == "__main__":
    print(char_data)

    c = Character("knight", **deepcopy(char_data["knight"]))
    print(c.get_stat("str"))
    c.set_stat("str", 5)
    c.add_to_stat("dex", 1)
    print(c.get_stat("str"))
    print(c.get_stat("dex"))
    c.add_temp_stat("weak", 5)
    c.add_temp_stat("weak", -2)
    print(c.get_temp_stat("weak"))
    c.add_temp_stat("weak", -3)
    print(c.get_temp_stat("weak"))
    c.add_temp_stat("weak", 5)
    c.remove_temp_stat("weak")
    print(c.temp_stats)
    print(c.max_hp, c.current_hp)
    c.current_hp = 85
    print(c.current_hp)
    # c.get_stat("test")
    # c.set_stat("foo", 5)
