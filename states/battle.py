import random
import pygame
from entities.characters import generate_char, Character
from entities.enemies import generate_enemy, Enemy
from cards.cards import generate_card, Card
from states.states import BattleState, PlayerTurnState


class BattleStateMachine:
    def __init__(self, player: Character, deck: list[Card]):
        self.current_state = BattleState.BATTLE_START
        self.setup_done = False
        self.deck = deck
        self.enemies: list[Enemy] = []
        self.selected_card: Card = None
        self.target_enemy: Enemy = None
        self.player_turn_state = PlayerTurnState.TURN_START
        self.enemy_action_idx = 0
        self.player = player

    def update(self, events: list[pygame.event.Event]):
        if self.current_state == BattleState.BATTLE_START:
            self._battle_start(events)
        elif self.current_state == BattleState.PLAYER_TURN:
            self._player_turn(events)
        elif self.current_state == BattleState.ENEMY_TURN:
            self._enemy_turn(events)
        elif self.current_state == BattleState.BATTLE_END:
            self._battle_end(events)

    def _battle_start(self, events: list[pygame.event.Event]):
        print("Battle start")
        if not self.setup_done:
            self.draw_pile = self.deck.copy()
            random.shuffle(self.draw_pile)
            self.discard_pile = []
            self.exhaust_pile = []
            self.hand = []
            self.max_player_energy = self.player.max_energy
            self.curr_player_energy = self.max_player_energy

            # Select encounter from pool.
            # In this case, we just take a default
            enemy_list = ["worm"]
            for enemy in enemy_list:
                self.enemies.append(generate_enemy(enemy))
            self.setup_done = True
        self.current_state = BattleState.PLAYER_TURN

    def _player_turn(self, events: list[pygame.event.Event]):
        if self.player_turn_state == PlayerTurnState.TURN_START:
            self._player_turn_start(events)
        elif self.player_turn_state == PlayerTurnState.SELECT_CARD:
            self._select_card(events)
        elif self.player_turn_state == PlayerTurnState.SELECT_TARGET:
            self._select_target(events)
        elif self.player_turn_state == PlayerTurnState.PLAY_CARD:
            self._play_card(events)
        elif self.player_turn_state == PlayerTurnState.TURN_END:
            self._player_turn_end(events)

    def _player_turn_start(self, events: list[pygame.event.Event]):
        print("Start player turn")
        for enemy in self.enemies:
            enemy.choose_intent()
        self._draw_cards(5)
        if not self.hand:
            # Empty hand after even reshuffling? Game over.
            self.player_turn_state = PlayerTurnState.TURN_END
            self.current_state = BattleState.BATTLE_END
        # Simple energy assignment for now
        self.curr_player_energy = self.max_player_energy
        self.player_turn_state = PlayerTurnState.SELECT_CARD

    def _select_card(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Implement mouse clicking later.
                pass
            elif event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    # Direct selection via keyboard
                    # Use K_1 so that K_0 picks the last one.
                    num = event.key - pygame.K_1
                    if len(self.hand) > num:
                        if self.hand[num].cost > self.curr_player_energy:
                            print("Not enough energy!")
                            continue
                        self.selected_card = self.hand[num]
                        print(f"Selected: {self.selected_card}")
                        self.player_turn_state = PlayerTurnState.SELECT_TARGET
                elif event.key == pygame.K_e:
                    print("End turn")
                    self.player_turn_state = PlayerTurnState.TURN_END

    def _select_target(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Implement mouse clicking later.
                pass
            elif event.type == pygame.KEYDOWN:
                if pygame.K_0 <= event.key <= pygame.K_9:
                    # Direct selection via keyboard
                    # Use K_1 so that K_0 picks the last one.
                    num = event.key - pygame.K_1
                    if len(self.enemies) > num:
                        self.target_enemy = self.enemies[num]
                        print(f"Target_enemy: {self.target_enemy}")
                        self.player_turn_state = PlayerTurnState.PLAY_CARD
                elif event.key == pygame.K_ESCAPE:
                    # Clear card selection and return to SELECT_CARD
                    self.selected_card = None
                    self.player_turn_state = PlayerTurnState.SELECT_CARD

    def _play_card(self, events: list[pygame.event.Event]):
        # In here, we'd call the selected card logic.
        # CAREFUL HERE!
        self.curr_player_energy -= self.selected_card.cost
        print(f"Hand before: {self.hand}")
        print(f"Discard pile before: {self.discard_pile}")
        self.selected_card.execute_effect(self.player, self.target_enemy)
        self.hand.remove(self.selected_card)  # Works if card instances are unique
        self.discard_pile.append(self.selected_card)
        self.selected_card = None
        self.target_enemy = None
        print(f"Hand after: {self.hand}")
        print(f"Discard pile after: {self.discard_pile}")
        self.enemies = [e for e in self.enemies if e.current_hp > 0]
        if not self.enemies:
            # Won battle
            self.current_state = BattleState.BATTLE_END
        else:
            self.player_turn_state = PlayerTurnState.SELECT_CARD

    def _player_turn_end(self, events: list[pygame.event.Event]):
        # Discard card if selected, just in case.
        if self.selected_card:
            self.hand.remove(self.selected_card)  # Works if card instances are unique
            self.discard_pile.append(self.selected_card)
        # Discard remaining cards on hand
        while self.hand:
            self.discard_pile.append(self.hand.pop())
        # Clear selections
        self.selected_card = None
        self.target_enemy = None
        self.current_state = BattleState.ENEMY_TURN
        # Setting player's turn to start so it won't auto end the turn again.
        self.player_turn_state = PlayerTurnState.TURN_START

    def _enemy_turn(self, events):
        print(self.current_state)
        print(self.enemy_action_idx, len(self.enemies))
        if self.enemy_action_idx < len(self.enemies):
            enemy = self.enemies[self.enemy_action_idx]
            enemy.execute_intent(self.player)
            if self.player.current_hp <= 0:
                self.current_state = BattleState.BATTLE_END
                return
            self.enemy_action_idx += 1
        else:
            # All enemies have acted, end the turn.
            print("Reached turn end")
            self.enemy_action_idx = 0
            self.current_state = BattleState.PLAYER_TURN

    def _battle_end(self, events):
        if self.player.current_hp > 0:
            print("You win!")
        else:
            print("You lose...")
        # Clear everything.
        self.hand.clear()
        self.draw_pile.clear()
        self.discard_pile.clear()
        self.exhaust_pile.clear()
        self.selected_card = None
        self.target_enemy = None
        self.enemy_action_idx = 0
        self.setup_done = False

    def _draw_cards(self, draw_num: int):
        if not self.draw_pile:
            # Try to reshuffle discard pile.
            self._reshuffle()
        if not self.draw_pile:
            # Player would have 0 cards on hand. Return early.
            return
        for _ in range(draw_num):
            if self.draw_pile:
                if len(self.hand) < 10:
                    self.hand.append(self.draw_pile.pop())
                else:
                    self.discard_pile.append(self.draw_pile.pop())

    def _reshuffle(self):
        for _ in range(len(self.discard_pile)):
            self.draw_pile.append(self.discard_pile.pop())
        random.shuffle(self.draw_pile)


def render_debug_text(text):
    return pygame.font.SysFont("arial", 18).render(text, True, (0, 0, 0))


def render_battle_state(screen, battle_sm: BattleStateMachine):
    x = 10
    screen.blit(render_debug_text(str(battle_sm.current_state)), (x, 0))
    screen.blit(render_debug_text(str(battle_sm.player_turn_state)), (x, 16))
    if battle_sm.selected_card:
        screen.blit(render_debug_text(f"Card: {battle_sm.selected_card.name}"), (x, 32))
    else:
        screen.blit(render_debug_text(f"No card selected."), (x, 32))
    if battle_sm.target_enemy:
        name = battle_sm.target_enemy.name
        hp = battle_sm.target_enemy.current_hp
        screen.blit(render_debug_text(f"Target: {name} - {hp} HP"), (x, 48))
    else:
        screen.blit(render_debug_text(f"No enemy selected."), (x, 48))
    if battle_sm.player:
        hp = battle_sm.player.current_hp
        screen.blit(render_debug_text(f"Player HP: {hp}"), (x, 64))
    x = 1000
    y = 0
    for enemy in battle_sm.enemies:
        name = enemy.name
        hp = enemy.current_hp
        screen.blit(render_debug_text(f"Enemy: {name} - {hp} HP"), (x, y))
        for intent in enemy.current_intents:
            name, val = intent
            screen.blit(render_debug_text(f"Intent: {name} ({val})"), (x, y + 16))
            y += 16
        y += 32


sample_deck = [
    generate_card("strike"),
    # generate_card("defend"),
    generate_card("bash"),
]

player = generate_char("knight")

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

battle = None
active_battle = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    screen.fill("gray45")
    if not battle and active_battle:
        battle = BattleStateMachine(player, sample_deck)
    if battle:
        if battle.current_state == BattleState.BATTLE_END:
            render_battle_state(screen, battle)
            battle.update(events)
            battle = None
            active_battle = False
            continue
        render_battle_state(screen, battle)
        battle.update(events)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
