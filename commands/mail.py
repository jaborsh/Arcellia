import re
from datetime import datetime

from evennia import ObjectDB
from evennia.comms.models import Msg
from evennia.utils import create, make_iter
from evennia.utils.evmenu import EvMenu

from commands.command import Command

__all__ = ("CmdMail",)


class CmdMail(Command):
    """
    Syntax: mail
            mail [player,player,...]

    'Mail' displays the contents of your mailbox. If you specify one or more
    players, separated by commas if more than one, you will begin composing
    a letter to those individuals.
    """

    key = "mail"
    locks = "cmd:all()"
    help_category = "General"

    def func(self):
        caller = self.caller
        args = self.args.strip()
        if not args:
            # View Mail
            mail = Msg.objects.get_by_tag(category="mail").filter(
                db_receivers_objects=caller
            )
            if not mail:
                caller.msg("You have no mail.")
                return

            caller.msg(
                "You have the following letters:\n"
                + "\n".join(
                    [
                        f"  |w{index + 1}|n: {letter.header.strip()}"
                        for index, letter in enumerate(mail)
                    ]
                )
            )

            MailMenu(
                caller,
                "commands.mail",
                startnode="view_mail",
                cmdset_mergetype="Replace",
                cmdset_priority=1,
                auto_quit=True,
                cmd_on_exit="look",
                persistent=False,
                inbox=mail,
            )
        else:
            namelist = [name.strip() for name in args.split(",")]
            nameregex = r"|".join(
                r"^%s$" % re.escape(name) for name in make_iter(namelist)
            )
            matches = ObjectDB.objects.filter(db_key__iregex=nameregex)
            if not matches:
                return caller.msg("No characters found by that name.")

            MailMenu(
                caller,
                "commands.mail",
                startnode="subject_mail",
                cmdset_mergetype="Replace",
                cmdset_priority=1,
                auto_quit=True,
                cmd_on_exit="look",
                persistent=False,
                targets=matches,
            )


def view_mail(caller, raw_input, **kwargs):
    """
    View the contents of the caller's mailbox.
    """
    text = "Select a letter to read, |w[D]|nelete letters, or |w[Q]|nuit: "
    options = (
        {
            "key": "_default",
            "goto": read_mail,
        },
        {
            "key": "d",
            "goto": "delete_mail",
        },
        {
            "key": "q",
            "goto": "node_quit",
        },
    )
    return text, options


def read_mail(caller, raw_input, **kwargs):
    """
    Read a letter.
    """
    try:
        caller.msg(caller.ndb._evmenu.inbox[int(raw_input) - 1].message)
    except Exception:
        caller.msg("An error has occurred.")
    return "view_mail"


def delete_mail(caller, raw_input, **kwargs):
    """
    Delete a letter.
    """
    text = (
        "Select letters to delete (separate with commas or use - to specify a range): "
    )
    options = (
        {
            "key": "_default",
            "goto": confirm_delete,
        },
    )
    return text, options


def confirm_delete(caller, raw_input, **kwargs):
    """
    Perform deletion
    """
    try:
        # Parsing the input
        indices_to_delete = set()
        for part in raw_input.split(","):
            if "-" in part:
                start, end = map(int, part.split("-"))
                indices_to_delete.update(range(start, end + 1))
            else:
                indices_to_delete.add(int(part))

        # Adjusting indices to 0-based and performing deletion
        inbox = caller.ndb._evmenu.inbox
        for index in sorted(indices_to_delete, reverse=True):
            # Adjusting for 1-based input
            if 1 <= index <= len(inbox):
                inbox[index - 1].delete()

        # Update the inbox and notify the caller
        caller.ndb._evmenu.inbox = Msg.objects.get_by_tag(category="mail").filter(
            db_receivers_objects=caller
        )
        caller.msg(
            "You have the following letters:\n"
            + "\n".join(
                f"  |w{index + 1}|n: {letter.header.strip()}"
                for index, letter in enumerate(caller.ndb._evmenu.inbox)
            )
        )
        return "view_mail"
    except ValueError:
        caller.msg(
            "Invalid input. Please specify letter numbers to delete, separated by commas or a range with a hyphen."
        )
        return "view_mail"


def subject_mail(caller, raw_input, **kwargs):
    """
    Subject a letter.
    """
    text = "Subject: "
    options = (
        {
            "key": "_default",
            "goto": "compose_mail",
        },
    )
    return text, options


def compose_mail(caller, raw_input, **kwargs):
    """
    Compose a letter.
    """
    current_date = datetime.now().strftime("%H:%M:%S %p, %A, %B %d, %Y")
    recipients = caller.ndb._evmenu.targets
    caller.ndb._evmenu.subject = raw_input.strip()
    caller.ndb._evmenu.letter = ""
    caller.ndb._evmenu.lines = 0
    text = (
        f"From: {caller.display_name}\n"
        f"To: {', '.join([recipient.display_name for recipient in recipients])}\n"
        f"Date: {current_date}\n"
        f"Subject: {raw_input}\n"
        "Compose your letter. When you are finished, type ** on an empty line."
    )

    options = (
        {
            "key": "_default",
            "goto": "continue_mail",
        },
    )
    return text, options


def continue_mail(caller, raw_input, **kwargs):
    """
    Continue the letter draft.
    """
    caller.ndb._evmenu.letter += raw_input
    caller.ndb._evmenu.lines += 1
    text = str(caller.ndb._evmenu.lines) + "| " + raw_input.strip()
    options = (
        {
            "key": "_default",
            "goto": "continue_mail",
        },
        {
            "key": "**",
            "goto": "finalize_mail",
        },
    )

    return text, options


def finalize_mail(caller, raw_input, **kwargs):
    """
    Finalize the letter draft.
    """
    text = (
        "|w[L]|nook at your letter.\n"
        "|w[D]|nelete your letter and start over.\n"
        "|w[S]|nend your letter.\n"
        "|w[Q]|nuit."
    )
    options = (
        {
            "key": "l",
            "goto": review_letter,
        },
        {
            "key": "d",
            "goto": delete_letter,
        },
        {
            "key": "s",
            "goto": send_letter,
        },
        {
            "key": "q",
            "goto": "node_quit",
        },
    )
    return "|/" + text, options


def review_letter(caller, raw_input, **kwargs):
    """
    Review the letter draft.
    """
    caller.msg(caller.ndb._evmenu.letter.strip())
    return "finalize_mail"


def delete_letter(caller, raw_input, **kwargs):
    """
    Delete the letter draft.
    """
    caller.ndb._evmenu.letter = ""
    return "compose_mail"


def send_letter(caller, raw_input, **kwargs):
    """
    Send the letter.
    """
    recipients = caller.ndb._evmenu.targets
    letter = caller.ndb._evmenu.letter
    subject = caller.ndb._evmenu.subject
    caller.msg(f"Subject: {caller.ndb._evmenu.subject}")
    for recipient in recipients:
        recipient.msg(f"You have received a letter from {caller.display_name}.")
        new_message = create.create_message(
            caller, letter, receivers=recipient, header=subject
        )
        new_message.tags.add("new", category="mail")

    if recipients:
        string = "Mail sent successfully to:\n"
        string += "\n".join([f"  {recipient.display_name}" for recipient in recipients])
    else:
        string = "No recipients found."

    caller.msg(string)

    return "node_quit"


def node_quit(caller, raw_input, **kwargs):
    return "", None


class MailMenu(EvMenu):
    """
    Modified EvMenu for displaying mail.
    """

    def options_formatter(self, optionslist):
        """
        Formats the option block.

        Args:
            optionlist (list): List of (key, description) tuples for every
                option related to this node.

        Returns:
            options (str): The formatted option display.

        """

        return ""

    def node_formatter(self, nodetext, optionstext):
        """
        Formats the entirety of the node.

        Args:
            nodetext (str): The node text as returned by `self.nodetext_formatter`.
            optionstext (str): The options display as returned by `self.options_formatter`.
            caller (Object, Account or None, optional): The caller of the node.

        Returns:
            node (str): The formatted node to display.

        """

        return nodetext
