import pygame
import os
from dataclasses import dataclass, asdict, field
from entities.characters import generate_char
from cards.cards import generate_card

DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class GameState:
    running: bool = True
    user_turn: bool = True  # flips every single turn
    user_energy: int = 0
    draw_pile: list = field(default_factory=list)
    discard_pile: list = field(default_factory=list)
    exhaust_pile: list = field(default_factory=list)


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("S-Py-re")
clock = pygame.time.Clock()
game_state = GameState()

u_event = pygame.event.custom_type()
END_ENEMY_TURN = 1


def handle_keydown(event: pygame.event.Event):
    match event.key:
        case pygame.K_e:
            if game_state.user_turn:
                game_state.user_turn = False
                # For now, immediately send the event for the enemy turn.
                enemy_turn_end = pygame.event.Event(u_event, u_type=END_ENEMY_TURN)
                pygame.time.set_timer(enemy_turn_end, 3000)
        case _:
            return
    # Debugging
    render_game_state()


def handle_user_events(event: pygame.event.Event):
    if event.u_type == END_ENEMY_TURN:
        game_state.user_turn = True
        # This will be the character's max energy.
        game_state.user_energy = 3


def poll_events(game_state: GameState):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state.running = False
        elif event.type == pygame.KEYDOWN:
            handle_keydown(event)
        elif event.type == u_event:
            handle_user_events(event)


def render_debug_text(text):
    return pygame.font.SysFont("arial", 18).render(text, True, (0, 0, 0))


def render_game_state():
    x = 10
    screen.blit(render_debug_text("Game State"), (x, 0))
    y = 24
    for key, value in asdict(game_state).items():
        screen.blit(render_debug_text(f" - {key}: {value}"), (x, y))
        y += 16


def render_room():
    """Render using placeholder assets. For testing only."""
    bg = pygame.image.load(os.path.join(DIR, "assets/placeholder_room.png"))
    screen.blit(bg, (0, 0))


def render_player():
    """Render using placeholder assets. For testing only."""
    bg = pygame.image.load(os.path.join(DIR, "assets/placeholder_player.png"))
    bg = bg.convert()
    bg.set_colorkey((255, 255, 255))
    screen.blit(bg, (screen.get_width() // 4, screen.get_height() // 4))


def render_energy(character):
    bg = pygame.image.load(os.path.join(DIR, "assets/placeholder_energy.png"))
    bg = bg.convert()
    bg.set_colorkey((255, 255, 255))
    txt = pygame.font.SysFont("arial", 18).render(
        f"{character.current_energy}/{character.max_energy}", True, (0, 0, 0)
    )
    bg.blit(txt, (bg.get_width() / 2, bg.get_height() / 4))
    screen.blit(bg, (screen.get_width() // 4, 3 * screen.get_height() // 4))


def render_enemy():
    """Render using placeholder assets. For testing only."""
    bg = pygame.image.load(os.path.join(DIR, "assets/placeholder_enemy.png"))
    bg = bg.convert()
    bg.set_colorkey((255, 255, 255))
    screen.blit(bg, (3 * screen.get_width() // 4, 2 * screen.get_height() // 4))


player = generate_char("knight")
card = generate_card("strike")

while game_state.running:
    poll_events(game_state)

    # fill the screen to wipe last frame
    render_room()
    render_player()
    render_enemy()
    screen.blit(card.render_card(), (screen.get_width() // 2, screen.get_height() // 2))
    render_energy(player)
    render_game_state()

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
