def add_gold(game, gold):
    game.player.gold += gold


EVENT_FUNC = {
    "add_gold": add_gold,
}
