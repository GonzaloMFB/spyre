import pygame
from states.states import GameState


class GameStateMachine:
    def __init__(self):
        self.current_state = GameState.MAP  # Change to title when the game loads

    def update(self, events: list[pygame.event.Event]):
        if self.current_state == GameState.TITLE_SCREEN:
            self._title_screen(events)
        elif self.current_state == GameState.CHARACTER_SELECT:
            self._character_select(events)
        elif self.current_state == GameState.MAP:
            self._map(events)
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

    def _title_screen(events: list[pygame.event.Event]):
        pass

    def _character_select(events: list[pygame.event.Event]):
        pass

    def _map(events: list[pygame.event.Event]):
        pass


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
