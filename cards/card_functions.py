from entities.characters import Character
from entities.enemies import Enemy


def damage(player: Character, target: Enemy, value: int):
    if player.get_temp_stat("weak"):
        value = int(value * 0.75)
    target.damage(value)


def block(player: Character, value: int):
    if player.get_temp_stat("frail"):
        value = int(value * 0.75)
    player.block += value


def apply_vuln(target: Enemy, value: int):
    target.add_temp_stat("vulnerable", value)


# Map format is (function, needs_player, needs_target)
CARD_FUNC = {
    "damage": (damage, True, True),
    "block": (damage, True, False),
    "apply_vuln": (apply_vuln, False, True),
}
