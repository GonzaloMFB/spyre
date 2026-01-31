import pygame
import os
from dataclasses import dataclass, asdict, field
from entities.characters import generate_char
from entities.enemies import generate_enemy, Enemy
from cards.cards import generate_card, Card

DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class GameState:
    running: bool = True
    user_turn: bool = True  # flips every single turn
    user_energy: int = 0
    in_battle: bool = False
    draw_pile: list[Card] = field(default_factory=list)
    discard_pile: list[Card] = field(default_factory=list)
    exhaust_pile: list[Card] = field(default_factory=list)
    current_enemies: list[Enemy] = field(default_factory=list)


def render_debug_text(text):
    return pygame.font.SysFont("arial", 18).render(text, True, (0, 0, 0))


def render_game_state():
    x = 10
    screen.blit(render_debug_text("Game State"), (x, 0))
    y = 24
    for key, value in game_state.__dict__.items():
        screen.blit(render_debug_text(f" - {key}: {value}"), (x, y))
        y += 16


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
        case pygame.K_RETURN:
            print("Starting battle")
            game_state.in_battle = True
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


def player_turn():
    print("Player turn")


def enemy_turn():
    # Enemy turns are simple:
    # * Read all enemies in the battle.
    # * Run their behavior function, which will handle different intents.
    for enemy in game_state.current_enemies:
        enemy.behavior()


def battle_loop():
    debug_ctr = 0
    if game_state.in_battle:
        print("Battle start!")
    while game_state.in_battle and debug_ctr < 5:
        # Player turn
        player_turn()
        # AI turn
        enemy_turn()
        debug_ctr += 1
        if debug_ctr >= 5:
            game_state.in_battle = False
            print("Battle end")


player = generate_char("knight")
card = generate_card("strike")
sample_enemy = generate_enemy("worm")
game_state.current_enemies.append(sample_enemy)

while game_state.running:
    poll_events(game_state)

    screen.fill("gray45")
    render_game_state()
    battle_loop()

    pygame.display.flip()
    clock.tick(60)  # limits FPS to 60

pygame.quit()
