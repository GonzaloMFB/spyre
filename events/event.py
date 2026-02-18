import json
import random
import os

import pygame

from utils.utils import render_debug_text

DIR = os.path.dirname(os.path.abspath(__file__))

EVENT_WINDOW_SIZE = (900, 506)


def fetch_game_event():
    event_data_path = os.path.join(DIR, "event_data.json")
    with open(event_data_path, "r") as f:
        event_data = json.load(f)
    if not isinstance(event_data, list):
        return {}
    return random.choice(event_data)


class GameEvent:
    def __init__(self):
        self.data = fetch_game_event()
        self.has_chosen = False
        self.complete = False
        self.window = pygame.surface.Surface(EVENT_WINDOW_SIZE)

    def render_event(self, screen):
        # Render square
        self.window.fill("white")
        if not self.has_chosen:
            # Render text and options
            self.window.blit(render_debug_text(self.data.get("event_text")), (0, 0))
            for i, choice in enumerate(self.data.get("choices")):
                self.window.blit(
                    render_debug_text(choice.get("choice_text")), (0, 16 * (i + 1))
                )
        else:
            self.window.blit(render_debug_text(self.data.get("event_text")), (0, 0))
        screen.blit(self.window, (0, 0))


if __name__ == "__main__":
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    game_event = GameEvent()
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        screen.fill("gray45")
        game_event.render_event(screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()
