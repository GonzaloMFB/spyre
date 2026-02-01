import random

"""
Enemy intents can combine multiple actions, e.g. damage X and block Y this turn.
The intents array contains tuples with the function name and its base value.
Upon execution of the function in enemy_functions.py, we run the necessary modifiers.
"""


def worm():
    actions = [
        [("damage", 8)],
        [("block", 4)],
        [("buff_str", 6)],
    ]
    return random.choice(actions)


INTENT_MAP = {
    "worm": worm,
}
