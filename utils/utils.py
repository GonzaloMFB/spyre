import pygame

WINDOW_SIZE = (1280, 720)


def render_debug_text(text, color=None):
    if not color:
        color = (0, 0, 0)
    return pygame.font.SysFont("arial", 18).render(text, True, color)
