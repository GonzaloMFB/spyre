from entities.characters import Character


def damage(user, target: Character, value: int):
    if user.get_temp_stat("weak"):
        value = int(value * 0.75)
    strength = user.get_stat("str")
    target.damage(value + strength)


def block(user, value: int):
    if user.get_temp_stat("frail"):
        value = int(value * 0.75)
    user.block += value


def buff_strength(user, value: int):
    user.add_to_stat("str", value)


# Format is func, needs_user, needs_target
ENEMY_FUNC = {
    "damage": (damage, True, True),
    "block": (block, True, False),
    "buff_str": (buff_strength, True, False),
}
