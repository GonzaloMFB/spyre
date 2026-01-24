from entities.entity import Entity


class Enemy(Entity):
    def __init__(self, max_hp):
        super().__init__()
        self._max_hp = max_hp
        self._current_hp = self._max_hp
