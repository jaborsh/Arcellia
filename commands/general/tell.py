from evennia.utils import (
    create,
)

from commands.command import Command
from server.conf import logger


class CmdTell(Command):
    """
    Syntax: tell <character> <message>                 # regular tells
            tell <character>,<character>,... <message> # multiple characters tell
            tell <character> ;<emote>                  # emoted tells
            tell <character>,<character>,... ;<emote>  # multiple characters emote

    Example: tell jake,john Hi there!

    Send a message to a character if online. If no argument is given, you
    will receive your most recent message. If sending to multiple
    characters, separate names with commas.
    """

    key = "tell"
    locks = "cmd:all()"
    help_category = "General"

    def _send_message(self, caller, content, receivers, is_emote=False):
        """
        Sends a message to a list of receivers.

        Args:
            caller (Object): The object sending the message.
            content (str): The message content.
            receivers (list): A list of objects to receive the message.
            is_emote (bool, optional): Whether the message is an emote. Defaults to False.
        """  # noqa: E501
        create.create_message(caller, content, receivers=receivers)

        received = []
        rstrings = []
        for target in receivers:
            if not target.access(caller, "msg"):
                rstrings.append(
                    f"You are not allowed to send tells to {target.get_display_name(caller)}."  # noqa: E501
                )
                continue

            if caller == target:
                rstrings.append("Telepathy isn't for inner monologues!")
                continue

            if is_emote:
                target.msg(
                    "Silently from %s: %s"
                    % (caller.get_display_name(target), content)
                )
                logger.log_file(
                    "Silently from %s: %s"
                    % (caller.get_display_name(target), content),
                    filename=f"{target.log_folder}/tells.log",
                )
            else:
                target.msg(
                    f"{caller.get_display_name(target)} tells you: {content}"
                )
                logger.log_file(
                    f"{caller.get_display_name(target)} tells you: {content}",
                    filename=f"{target.log_folder}/tells.log",
                )
            if hasattr(target, "sessions") and not target.sessions.count():
                rstrings.append(
                    f"{target.get_display_name(caller)} is not awake."
                )
            else:
                received.append(f"{target.get_display_name(caller)}")

        if rstrings:
            self.msg("\n".join(rstrings))

        if not received:
            return

        if is_emote:
            self.msg("Silently to %s: %s" % (", ".join(received), content))
            logger.log_file(
                "Silently to %s: %s" % (", ".join(received), content),
                filename=f"{caller.log_folder}/tells.log",
            )
        else:
            self.msg("You tell %s: %s" % (", ".join(received), content))
            logger.log_file(
                "You tell %s: %s" % (", ".join(received), content),
                filename=f"{caller.log_folder}/tells.log",
            )

    def func(self):
        caller = self.caller

        if not self.args:
            # No argument, show latest messages.
            return self.msg("Syntax: tell <character[s]> <message>")

        args = self.args.strip().split(" ", 1)
        targets, message = args[0].split(","), args[1]

        receivers = [
            caller.search(target, quiet=True, global_search=True)[0]
            for target in targets
            if caller.search(target, quiet=True, global_search=True)
        ]

        message = message.strip()

        if not receivers:
            return self.msg("Who do you want to tell?")

        if not message:
            return self.msg("What do you want to tell them?")

        if message.startswith(";"):
            # Emoted tell
            emote = message[1:].strip()
            if not emote:
                return self.msg("What do you want to emote to them?")
            self._send_message(
                caller, f"{caller.name} {emote}", receivers, is_emote=True
            )
        else:
            # Regular tell
            message = message.strip()
            self._send_message(caller, message, receivers)
