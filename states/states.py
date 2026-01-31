from enum import Enum


class GameState(Enum):
    TITLE_SCREEN = 0
    CHARACTER_SELECT = 1
    ROOM = 2
    # ROOM SHOULD BE ABLE TO OVERLAY:
    # BATTLE
    # EVENT
    # SHOP
    # MAP
    # CAMP, maybe
    # SETTINGS
    CLOSE_GAME = 3


class BattleState(Enum):
    BATTLE_START = 0
    PLAYER_TURN = 1
    ENEMY_TURN = 2
    BATTLE_END = 3


class PlayerTurnState(Enum):
    TURN_START = 0
    SELECT_CARD = 1
    SELECT_TARGET = 2
    PLAY_CARD = 3
    TURN_END = 4
