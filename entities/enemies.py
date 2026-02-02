import csv
import os
from copy import deepcopy
from entities.entity import Entity
from entities.enemy_intents import INTENT_MAP
from entities.enemy_functions import ENEMY_FUNC

DIR = os.path.dirname(os.path.abspath(__file__))


def default_behavior():
    print("Hello! I am the default behavior")


class Enemy(Entity):
    def __init__(self, name, base_hp):
        super().__init__(base_hp)
        self.name = name
        self.current_intents = []

    def execute_intent(self, player):
        # Placeholder for now.
        print("Executing intent")
        for intent in self.current_intents:
            name, val = intent
            print(f"{name}, {val}")
            # Could optimize later by not passing player and enemy.
            func, needs_user, needs_target = ENEMY_FUNC[name]
            if needs_user and needs_target:
                func(self, player, val)
            elif needs_user:
                func(self, val)
            elif needs_target:
                func(player, val)
            else:
                func(val)

    def choose_intent(self):
        self.current_intents = INTENT_MAP[self.name]()


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
