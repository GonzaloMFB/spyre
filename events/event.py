import json
import random
import os

import pygame

from events.event_func import EVENT_FUNC
from scenes.topbar import TOPBAR_SIZE
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
        self.outcomes: list[TextBox] = []
        self.cont_coords = None
        self.continue_button = pygame.image.load(
            os.path.join(DIR, "../assets/placeholder_continue.png")
        )
        self.window_rect = pygame.Rect(0, TOPBAR_SIZE[1], *EVENT_WINDOW_SIZE)
        self.chosen = -1
        for idx, entry in enumerate(self.data.get("choices")):
            origin = (
                50,
                3 * self.window.get_height() // 4
                + idx * CHOICE_BOX_SIZE[1]
                + (idx * 10),
            )
            choice = TextBox(
                entry.get("choice_text"), CHOICE_BOX_SIZE, origin, clickable=True
            )
            outcome = TextBox(
                entry.get("outcome_text"), CHOICE_BOX_SIZE, origin, clickable=False
            )
            self.choices.append(choice)
            self.outcomes.append(outcome)

    def execute_effect(self, game, effect, val):
        func = EVENT_FUNC[effect]
        func(game, val)

    def is_continue_clicked(self, mouse_pos):
        if not self.cont_coords:
            print("No coords set")
            return False
        in_x = (
            self.cont_coords[0]
            <= mouse_pos[0]
            <= self.cont_coords[0] + self.continue_button.get_width()
        )
        in_y = (
            self.cont_coords[1]
            <= mouse_pos[1]
            <= self.cont_coords[1] + self.continue_button.get_height()
        )
        if in_x and in_y:
            print("Clicked continue box!")
            return True
        return False

    def render_event(self, screen):
        # Render square
        self.window.fill("white")
        title_sf = render_debug_text(self.data.get("title"))
        self.window.blit(
            title_sf,
            ((self.window.get_width() - title_sf.get_width()) // 2, 0),
        )
        event_text_sf = render_debug_text(self.data.get("event_text"))
        self.window.blit(
            event_text_sf,
            (50, (self.window.get_height() - event_text_sf.get_height()) // 2),
        )
        if not self.has_chosen:
            for _, box in enumerate(self.choices):
                self.window.blit(box.render(), (box.origin[0], box.origin[1]))
        else:
            box = self.outcomes[self.chosen]
            self.window.blit(box.render(), box.origin)
            self.cont_coords = (
                screen.get_width() - self.continue_button.get_width(),
                screen.get_height() // 2,
            )
            screen.blit(self.continue_button, self.cont_coords)
        screen.blit(self.window, self.window_rect)


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

    def is_clicked(self, mouse_pos):
        in_x = (
            self.origin[0] <= mouse_pos[0] <= self.origin[0] + self.surface.get_width()
        )
        in_y = (
            self.origin[1] <= mouse_pos[1] <= self.origin[1] + self.surface.get_height()
        )
        if self.clickable and in_x and in_y:
            print("Clicked choice box!")
            return True
        return False


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
