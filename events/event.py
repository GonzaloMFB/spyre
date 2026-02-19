import json
import random
import os

import pygame

from utils.utils import render_debug_text

DIR = os.path.dirname(os.path.abspath(__file__))

EVENT_WINDOW_SIZE = (900, 450)

CHOICE_BOX_SIZE = (600, 50)


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
        self.choices: list[TextBox] = []
        for idx, choice in enumerate(self.data.get("choices")):
            origin = (
                50,
                3 * self.window.get_height() // 4
                + idx * CHOICE_BOX_SIZE[1]
                + (idx * 10),
            )
            box = TextBox(
                choice.get("choice_text"), CHOICE_BOX_SIZE, origin, clickable=True
            )
            self.choices.append(box)

    def render_event(self, screen):
        # Render square
        self.window.fill("white")
        title_sf = render_debug_text(self.data.get("title"))
        self.window.blit(
            title_sf, ((self.window.get_width() - title_sf.get_width()) // 2, 0)
        )
        event_text_sf = render_debug_text(self.data.get("event_text"))
        self.window.blit(
            event_text_sf,
            (50, (self.window.get_height() - event_text_sf.get_height()) // 2),
        )
        for _, box in enumerate(self.choices):
            self.window.blit(box.render(), box.origin)
        screen.blit(self.window, (0, 0))


class TextBox:
    def __init__(self, text, dimensions, origin, clickable=False):
        # Origin: top leftmost coord of the surface on parent surface
        self.text = text
        self.surface = pygame.surface.Surface(dimensions)
        self.origin = origin
        self.clickable = clickable

    def render(self, origin=None):
        # Fill with color for now and render the text on top.
        if not origin:
            origin = (10, self.surface.get_height() // 2)
        self.surface.fill("blue")
        self.surface.blit(render_debug_text(self.text), origin)
        return self.surface


class Title:
    def __init__(self):
        pass


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
