import pygame
from dataclasses import dataclass


@dataclass
class GameState:
    running: bool = True


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()


def poll_events(game_state: GameState):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False


def render():
    pass


game_state = GameState()

while game_state.running:
    poll_events(game_state)

    # fill the screen to wipe last frame
    screen.fill("green")

    render()

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
