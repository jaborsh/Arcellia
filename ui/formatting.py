import math
import re

from django.conf import settings
from evennia.utils.ansi import strip_ansi


def wrap(text, text_width=80, pre_text="", align="l", indent=0, hang=0):
    # Wrap the text to the terminal width.
    if not text:
        return ""

    text = text.lstrip()
    text_width = text_width if text_width else settings.CLIENT_DEFAULT_WIDTH
    final_text = []

    # Cache each manually determined line break
    text_lines = re.split(r"\n|\|/", text)
    for text_line in text_lines:
        line = ""
        line_list = []

        # Determine available characters.
        available_chars = text_width - len(strip_ansi(pre_text)) - hang

        # Cache each word in the line.
        word_list = re.findall(r"((?:\S+\s*)|(?:^\s+))", text_line)

        for word in word_list:
            # available_chars += (len(word) - len(strip_ansi(word)))
            if len(strip_ansi(word)) <= available_chars:
                line += word
                available_chars -= len(strip_ansi(word))

            # Catch words that are too long to fit on a line, for whatever reason.
            elif len(strip_ansi(word)) > text_width - len(strip_ansi(pre_text)):
                char_list = re.findall(
                    # r"(?:\|[0-5]{3}\w)|(?:\|\w{2})|(?:\S)", word
                    r"\|\[?([0-5][0-5][0-5]|\=?[rRyYgGcCbBmMwWxX]|#?[0-9a-f]{6})",
                    word,
                )
                for char in char_list:
                    if len(strip_ansi(char)) <= available_chars:
                        line += char
                        available_chars -= len(strip_ansi(char))
                    else:
                        line += "-"
                        line_list.append(line)
                        line = char
                        available_chars = (
                            text_width - len(pre_text) - len(strip_ansi(char))
                        )

            # If the word doesn't fit, start a new line.
            else:
                line_list.append(line)
                line = word
                available_chars = (
                    text_width - len(strip_ansi(pre_text)) - len(strip_ansi(word))
                )
        # Add the last line to the list.
        line_list.append(line)

        # Justify the text.

        for line in line_list:
            if not final_text:
                line_text = pre_text + justify(line, text_width, align, indent)
            else:
                line_text = justify(
                    line, text_width, align, len(strip_ansi(pre_text)), hang
                )
            final_text.append(line_text)

    return "\n".join(final_text) + "|n"


def justify(text, width, align, indent=0, hang=0):
    if align == "l":
        return " " * (indent + hang) + text
    elif align == "c":
        return (
            " " * math.ceil((width / 2) - (len(strip_ansi(text)) / 2) + indent) + text
        )

    return text
