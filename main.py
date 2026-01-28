import pygame
from dataclasses import dataclass, asdict


@dataclass
class GameState:
    running: bool = True
    user_turn: bool = True  # flips every single turn


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
game_state = GameState()


def handle_keydown(event: pygame.event.Event):
    match event.key:
        case pygame.K_e:
            if game_state.user_turn:
                game_state.user_turn = not game_state.user_turn
        case _:
            return


def poll_events(game_state: GameState):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False
        if event.type == pygame.KEYDOWN:
            handle_keydown(event)


def render_debug_text(text):
    return pygame.font.SysFont("arial", 18).render(text, True, (0, 0, 0))


def render_game_state(screen: pygame.surface.Surface):
    x = 10
    screen.blit(render_debug_text("Game State"), (x, 0))
    y = 24
    for key, value in asdict(game_state).items():
        screen.blit(render_debug_text(f" - {key}: {value}"), (x, y))
        y += 16


def render():
    pass


while game_state.running:
    poll_events(game_state)

    # fill the screen to wipe last frame
    screen.fill("gray45")

    render()
    render_game_state(screen)

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
