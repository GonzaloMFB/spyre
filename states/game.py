import pygame
from states.states import GameState
from scenes.map import Map, Node


class GameStateMachine:
    def __init__(self):
        self.current_state = GameState.ROOM  # Change to title when the game loads
        self.allow_navigation = True
        self.map_overlay_open = False
        self.deck_overlay_open = False
        self.settings_overlay_open = False
        self.act_map = Map()
        self.act_map.generate_map()

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
            pass
        elif self.current_state == GameState.BATTLE:
            pass
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
            self._handle_map_overlay(self, events)
        elif self.deck_overlay_open:
            pass
        elif self.settings_overlay_open:
            pass

    def _title_screen(self, events: list[pygame.event.Event]):
        pass

    def _character_select(self, events: list[pygame.event.Event]):
        pass

    def _handle_map_overlay(self, events: list[pygame.event.Event]):
        for event in events:
            if self.allow_navigation and event.type == pygame.MOUSEBUTTONDOWN:
                clicked_node = self._get_clicked_node()
                if clicked_node and self.act_map.can_navigate_to(clicked_node):
                    self.act_map.current_node = clicked_node
                    # TODO: Transition to node state.
                    self._transition_to_node_state(clicked_node)
                    self.map_overlay_open = False
                    self.allow_navigation = False
            elif event.type == pygame.KEYDOWN:
                # Map can be closed with escape or M.
                if event.key in [pygame.K_ESCAPE, pygame.K_m]:
                    self.map_overlay_open = False
        if self.allow_navigation:
            # TODO: User can click on connected nodes to navigate.
            pass

    def _get_clicked_node(self):
        pass

    def _transition_to_node_state(self, clicked_node: Node):
        if clicked_node.node_type in ["fight", "elite", "boss"]:
            self.current_state = GameState.BATTLE
        elif clicked_node.node_type == "event":
            self.current_state = GameState.EVENT
        elif clicked_node.node_type == "shop":
            self.current_state = GameState.SHOP


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    screen.fill("gray45")

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
