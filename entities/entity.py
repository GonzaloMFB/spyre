class Entity:
    """
    Basic template class for entities in a S-Py-re combat.
    """

    def __init__(self, base_hp):
        self.stats = {
            "str": 0,
            "dex": 0,
        }
        self.temp_stats = {}
        self.powers = {}
        self._max_hp = int(base_hp)
        self._current_hp = self._max_hp

    # =============== HP ===============
    @property
    def max_hp(self):
        return self._max_hp

    @property
    def current_hp(self):
        return self._current_hp

    @current_hp.setter
    def current_hp(self, val):
        if val < 0:
            raise ValueError("current_hp must be a positive int")
        self._current_hp = min(self.max_hp, val)

    @max_hp.setter
    def max_hp(self, val: int):
        if val < 1:
            raise ValueError("max_hp must be at least 1")
        self._max_hp = val
        self.current_hp = min(self._max_hp, self.current_hp)

    def damage(self, val: int):
        self.current_hp -= val

    def heal(self, val: int):
        self.current_hp += val

    # ============= Stats ==============

    def _check_stat(self, stat):
        if stat not in self.stats:
            raise ValueError(f"Unknown stat: {stat}")
        return True

    def add_to_stat(self, stat, amount):
        self._check_stat(stat)
        self.stats[stat] += amount

    def set_stat(self, stat: str, quantity: int):
        self._check_stat(stat)
        self.stats[stat] = quantity

    def get_stat(self, stat: str):
        self._check_stat(stat)
        return self.stats[stat]

    def get_temp_stat(self, temp_stat: str):
        """
        temp stats are mutable.
        """
        return self.temp_stats.get(temp_stat)

    def add_temp_stat(self, temp_stat: str, quantity: int):
        """
        Adds to temp stats (e.g. vulnerable, weak) that can appear/disappear.
        """
        val = self.temp_stats.get(temp_stat, 0) + quantity
        self.temp_stats[temp_stat] = val
        # Clean temporary stat if it becomes 0
        if self.temp_stats[temp_stat] <= 0:
            self.remove_temp_stat(temp_stat)

    def remove_temp_stat(self, temp_stat: str):
        self.temp_stats.pop(temp_stat, None)
