from evennia import TICKER_HANDLER as TickerHandler
from handlers.handler import Handler


class CombatHandler(Handler):
    combat_default = {
        "enemies": [],
        "target": None,
        "ticker": None,
        "ticker_duration": 4,
    }

    def __init__(self, obj, db_attribute="combat"):
        if not obj.attributes.get(db_attribute, None):
            obj.attributes.add(db_attribute, self.combat_default.copy())

        self.data = obj.attributes.get(db_attribute)
        self.db_attribute = db_attribute
        self.obj = obj

    def msg(self, message, broadcast=True, **kwargs):
        self.obj.location.msg_contents(
            message,
            from_obj=self.obj,
        )

    def add_enemy(self, enemy):
        if enemy not in self.data["enemies"]:
            self.data["enemies"].append(enemy)
            self._save()

    def remove_enemy(self, enemy):
        self.data["enemies"].remove(enemy)
        self._save()

    def get_target(self):
        if self.data["target"]:
            return self.data["target"]
        elif self.data["enemies"]:
            return self.data["enemies"][0]
        else:
            return None

    def set_target(self, target):
        self.data["target"] = target
        self._save()

    def start_combat(self):
        if self.data["ticker"]:
            return

        self.data["ticker"] = TickerHandler.add(
            self.data["ticker_duration"],
            self.obj.combat_tick,
            "combat",
            persistent=False,
        )

        self._save()
        self.obj.combat_tick()

    def check_stop_combat(self):
        enemies = [
            enemy
            for enemy in self.data["enemies"]
            if enemy.health.value > 0 and enemy.location == self.obj.location
        ]

        if not enemies:
            self.stop_combat()
            return True

        return False

    def stop_combat(self):
        TickerHandler.remove(
            self.data["ticker_duration"],
            self.obj.combat_tick,
            "combat",
            persistent=False,
        )

        for enemy in self.data["enemies"]:
            enemy.combat.remove_enemy(self.obj)

        self.data["enemies"] = []
        self.data["target"] = None
        self.data["ticker"] = None
        self._save()
        self.obj.msg("Combat ends.")

    def reset(self):
        self.data = self.combat_default.copy()
        self._save()
