from world.amenu import AMenu


class NautilusBrain:
    def interact(self):
        AMenu(
            self.caller,
            "world.tutorial.interactions.nautilus_brain",
            startnode="node_start",
            auto_look=True,
            auto_help=True,
            persistent=True,
            cmd_on_exit=None,
        )
