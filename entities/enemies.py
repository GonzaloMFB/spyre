import csv
import os
from copy import deepcopy
from entity import Entity

DIR = os.path.dirname(os.path.abspath(__file__))


class Enemy(Entity):
    def __init__(self, name, base_hp, behavior):
        super().__init__(base_hp)
        self.name = name


def load_enemy_data():
    """
    Loads enemy data in memory, stored by name
    """
    data = {}
    char_path = os.path.join(DIR, "enemies.csv")
    with open(char_path, "r", newline="\n") as reader:
        fieldnames = next(reader).strip().split("|")
        char_data = csv.DictReader(reader, fieldnames=fieldnames, delimiter="|")
        for char in char_data:
            name = char.pop("name")
            data[name] = char
    return data


enemy_data = load_enemy_data()


def generate_enemy(name: str):
    """
    Enemy factory.
    :param name: Enemy name
    """
    if name not in enemy_data:
        raise ValueError(f"Unknown enemy: {name}")
    print(f"Generating enemy: {name.title()}.")

    template = enemy_data[name]
    instance_data = deepcopy(template)
    return Enemy(name=name, **instance_data)


e = generate_enemy("worm")
print(e.max_hp)
print(e.current_hp)
