import pygame


def render_debug_text(text):
    return pygame.font.SysFont("arial", 18).render(text, True, (0, 0, 0))
