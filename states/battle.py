import random
import pygame
from entities.enemies import generate_enemy
from states.states import BattleState, PlayerTurnState


class BattleStateMachine:
    def __init__(self, deck: list):
        self.current_state = BattleState.BATTLE_START
        self.setup_done = False
        self.deck = deck
        self.enemies = []
        self.player_turn_state = PlayerTurnState.TURN_START

    def update(self):
        if self.current_state == BattleState.BATTLE_START:
            self._battle_start()
        elif self.current_state == BattleState.PLAYER_TURN:
            self._player_turn()
        elif self.current_state == BattleState.ENEMY_TURN:
            self._enemy_turn()
        elif self.current_state == BattleState.BATTLE_END:
            self._battle_end()

    def _battle_start(self):
        if not self.setup_done:
            self.draw_pile = self.deck.copy()
            random.shuffle(self.draw_pile)
            self.discard_pile = []
            self.exhaust_pile = []
            self.hand = []
            # Select encounter from pool.
            # In this case, we just take a default
            enemy_list = ["worm"]
            for enemy in enemy_list:
                self.enemies.append(generate_enemy(enemy))
            self.setup_done = True
        self.current_state = BattleState.PLAYER_TURN

    def _player_turn(self):
        if self.player_turn_state == PlayerTurnState.TURN_START:
            self._player_turn_start()
        elif self.player_turn_state == PlayerTurnState.SELECT_CARD:
            pass
        elif self.player_turn_state == PlayerTurnState.SELECT_TARGET:
            pass
        elif self.player_turn_state == PlayerTurnState.PLAY_CARD:
            pass
        elif self.player_turn_state == PlayerTurnState.TURN_END:
            pass

    def _player_turn_start(self):
        pass

    def _enemy_turn(self):
        pass

    def _battle_end(self):
        pass

    def _draw_cards(self, draw_num: int):
        if not self.draw_pile:
            # Try to reshuffle discard pile.
            self._reshuffle()
        if not self.draw_pile:
            # Player would have 0 cards on hand. Return early.
            return
        for _ in range(draw_num):
            if self.draw_pile:
                self.hand.append(self.draw_pile.pop())

    def _reshuffle(self):
        for _ in range(len(self.discard_pile)):
            self.draw_pile.append(self.discard_pile.pop())
        random.shuffle(self.draw_pile)


def render_debug_text(text):
    return pygame.font.SysFont("arial", 18).render(text, True, (0, 0, 0))


def render_battle_state(screen, battle_sm: BattleStateMachine):
    x = 10
    screen.blit(render_debug_text(str(battle_sm.current_state)), (x, 0))


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

battle = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("gray45")
    if not battle:
        battle = BattleStateMachine(["foo", "bar"])
    render_battle_state(screen, battle)
    battle.update()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
