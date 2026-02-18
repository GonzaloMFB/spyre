import pygame

from cards.cards import generate_card
from entities.characters import generate_char
from states.battle import BattleStateMachine
from states.states import GameState, BattleState


from scenes.map import Map, Node, NODE_SIZE

STARTER_DECKS = {"knight": {"strike": 5, "defend": 4, "bash": 1}}


def generate_deck(name):
    deck = []
    starter = STARTER_DECKS.get(name)
    for card_name, num in starter.items():
        for _ in range(num):
            deck.append(generate_card(card_name))
    return deck


class GameStateMachine:
    def __init__(self):
        # Base
        self.current_state = GameState.ROOM  # Change to title when the game loads
        # For now, init char here. Change it later on character select.
        player_class = "knight"
        self.player = generate_char(player_class)
        self.deck = generate_deck(player_class)

        # Map-related
        self.act_map = Map()
        self.act_map.generate_map()
        self.current_layer = 0
        self.curr_node = None
        self.allow_navigation = True
        self.map_overlay_open = False

        # Other overlays
        self.deck_overlay_open = False
        self.settings_overlay_open = False

        # Sub state machines
        self.battle_sm = None

    def update(self, events: list[pygame.event.Event]):
        # These are the ones we can open at any time.
        no_overlay_states = [
            GameState.TITLE_SCREEN,
            GameState.CHARACTER_SELECT,
            GameState.GAME_OVER,
            GameState.QUIT_GAME,
        ]
        if self.current_state not in no_overlay_states:
            self._handle_overlays(events)

        if self.current_state == GameState.TITLE_SCREEN:
            self._title_screen(events)
        elif self.current_state == GameState.CHARACTER_SELECT:
            self._character_select(events)
        elif self.current_state == GameState.ROOM:
            self._room(events)
        elif self.current_state == GameState.BATTLE:
            if not self.battle_sm:
                self.battle_sm = BattleStateMachine(self.player, self.deck)
            self._battle(events)
        elif self.current_state == GameState.SHOP:
            pass
        elif self.current_state == GameState.EVENT:
            pass
        elif self.current_state == GameState.REWARD:
            pass
        elif self.current_state == GameState.GAME_OVER:
            pass
        elif self.current_state == GameState.QUIT_GAME:
            pass

    def _handle_overlays(self, events: list[pygame.event.Event]):
        # Only 1 overlay open at a time
        if self.map_overlay_open:
            self._handle_map_overlay(events)
        elif self.deck_overlay_open:
            pass
        elif self.settings_overlay_open:
            pass

    def _title_screen(self, events: list[pygame.event.Event]):
        pass

    def _character_select(self, events: list[pygame.event.Event]):
        pass

    def _event(self, events: list[pygame.event.Event]):
        pass

    def _battle(self, events: list[pygame.event.Event]):
        self.battle_sm.update(events)
        if self.battle_sm.current_state == BattleState.BATTLE_END:
            # Clear battle and change status to room.
            # Need to call again to make sure the update for BATTLE_END happens.
            self.battle_sm.update(events)
            self.battle_sm = None
            self.current_state = GameState.ROOM

    def _room(self, events: list[pygame.event.Event]):
        for event in events:
            self._handle_map_open(event)

    def _handle_map_overlay(self, events: list[pygame.event.Event]):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.allow_navigation:
                clicked_node = self._get_clicked_node(event.pos)
                if clicked_node and self.act_map.can_navigate_to(
                    clicked_node, self.curr_node
                ):
                    self.curr_node = clicked_node
                    # TODO: Transition to node state.
                    self._transition_to_node_state(clicked_node)
                    self.map_overlay_open = False
                    self.allow_navigation = False

    def _get_clicked_node(self, mouse_pos):
        # Check node positions ONLY ABOVE CURRENT LAYER.
        # No need to interact with the other nodes.
        # Ignore last layer.
        target_layer = self.current_layer
        if target_layer > 0:
            # Allow users to click
            target_layer += 1
        if self.current_layer < len(self.act_map.layers) - 1:
            for node in self.act_map.layers[target_layer]:
                if not node:
                    continue
                if (
                    node.node_pos[0] <= mouse_pos[0] <= node.node_pos[0] + NODE_SIZE[0]
                ) and (
                    node.node_pos[1] <= mouse_pos[1] <= node.node_pos[1] + NODE_SIZE[1]
                ):
                    print("Clicked a valid Node!")
                    return node
        return None

    def _transition_to_node_state(self, clicked_node: Node):
        if clicked_node.node_type in ["fight", "elite", "boss"]:
            self.current_state = GameState.BATTLE
        elif clicked_node.node_type == "event":
            self.current_state = GameState.EVENT
        elif clicked_node.node_type == "shop":
            self.current_state = GameState.SHOP

    def _handle_map_open(self, event):
        if event.type == pygame.KEYDOWN:
            # Map
            if event.key == pygame.K_m:
                self.map_overlay_open = not self.map_overlay_open
            elif event.key == pygame.K_ESCAPE and self.map_overlay_open:
                self.map_overlay_open = False


def render_debug_text(text):
    return pygame.font.SysFont("arial", 18).render(text, True, (0, 0, 0))


def render_game_state(screen, game_sm: GameStateMachine):
    x = 10
    screen.blit(render_debug_text(str(game_sm.current_state)), (x, 0))
    screen.blit(render_debug_text(f"Map open? - {game_sm.map_overlay_open}"), (x, 16))
    pos_str = f"Current layer - {game_sm.current_layer}"
    screen.blit(render_debug_text(pos_str), (x, 32))


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

game_sm = GameStateMachine()

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    screen.fill("gray45")
    if game_sm:
        render_game_state(screen, game_sm)
        game_sm.update(events)
        if game_sm.map_overlay_open:
            game_sm.act_map.render_map(screen, game_sm.curr_node)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
