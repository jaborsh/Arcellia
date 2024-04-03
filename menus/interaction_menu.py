from evennia.utils.utils import dedent

from .amenu import AMenu


class InteractionMenu(AMenu):
    def nodetext_formatter(self, nodetext):
        """
        Format the node text itself.

        Args:
            nodetext (str): The full node text (the text describing the node).

        Returns:
            nodetext (str): The formatted node text.

        """

        text = nodetext.strip("\n")
        # if not text == "":
        text += "\n\n|CSelect an Option:|n"

        return dedent(text.strip("\n"), baseline_index=0).rstrip()
