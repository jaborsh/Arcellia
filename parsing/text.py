import math
import re

from django.conf import settings
from evennia.utils.utils import display_len, percentile, to_str

from parsing.colors import strip_ansi


def grammarize(message):
    """
    Corrects specific grammatical errors in the input message.
    """

    # Contraction apostrophe correction
    contractions = {
        r"\b(cant)\b": "can't",
        r"\b(couldnt)\b": "couldn't",
        r"\b(couldve)\b": "could've",
        r"\b(didnt)\b": "didn't",
        r"\b(doesnt)\b": "doesn't",
        r"\b(dont)\b": "don't",
        r"\b(hadnt)\b": "hadn't",
        r"\b(hasnt)\b": "hasn't",
        r"\b(im)\b": "I'm",
        r"\b(isnt)\b": "isn't",
        r"\b(itll)\b": "it'll",
        r"\b(ive)\b": "I've",
        r"\b(mightve)\b": "might've",
        r"\b(mustve)\b": "must've",
        r"\b(shouldnt)\b": "shouldn't",
        r"\b(shouldve)\b": "should've",
        r"\b(thats)\b": "that's",
        r"\b(theres)\b": "there's",
        r"\b(theyll)\b": "they'll",
        r"\b(theyre)\b": "they're",
        r"\b(wasnt)\b": "wasn't",
        r"\b(weve)\b": "we've",
        r"\b(wheres)\b": "where's",
        r"\b(whos)\b": "who's",
        r"\b(wouldve)\b": "would've",
    }

    for pattern, replacement in contractions.items():
        message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)

    # Multiple spaces
    message = re.sub(r" +", " ", message)

    # Capitalize standalone letter 'i'
    message = re.sub(r"\bi\b", "I", message)

    # Correcting use of a and an
    message = re.sub(r"\ba ([aeiou])", r"an \1", message, flags=re.IGNORECASE)

    # Unnecessary space before punctuation
    message = re.sub(r" ([.,;!?])", r"\1", message)

    # Add period if the message doesn't end with one
    if not message.endswith("."):
        message += "."

    # Capitalize the beginning of each sentence
    def capitalize_sentence(t):
        return t.group(0).capitalize()

    # Regex pattern to match the start of a sentence but not after an ellipsis
    pattern = r"(^[a-z])|(?<=[.!?]\s)(?<!\.\.\.\s)[a-z]"

    message = re.sub(pattern, capitalize_sentence, message)

    return message


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


def crop(text, width=None, suffix="[...]"):
    """
    Crop text to a certain width, throwing away text from too-long
    lines.

    Args:
        text (str): Text to crop.
        width (int, optional): Width of line to crop, in characters.
        suffix (str, optional): This is appended to the end of cropped
            lines to show that the line actually continues. Cropping
            will be done so that the suffix will also fit within the
            given width. If width is too small to fit both crop and
            suffix, the suffix will be dropped.

    Returns:
        text (str): The cropped text.

    """
    width = width if width else settings.CLIENT_DEFAULT_WIDTH
    ltext = len(strip_ansi(text))
    if ltext <= width:
        return text
    else:
        lsuffix = len(suffix)
        text = (
            text[:width]
            if lsuffix >= width
            else "%s%s" % (text[: width - lsuffix], suffix)
        )
        return to_str(text)


def format_grid(elements, width=78, sep="  ", verbatim_elements=None, line_prefix=""):
    """
    This helper function makes a 'grid' output, where it distributes the given
    string-elements as evenly as possible to fill out the given width.
    will not work well if the variation of length is very big!

    Args:
        elements (iterable): A 1D list of string elements to put in the grid.
        width (int, optional): The width of the grid area to fill.
        sep (str, optional): The extra separator to put between words. If
            set to the empty string, words may run into each other.
        verbatim_elements (list, optional): This is a list of indices pointing to
            specific items in the `elements` list. An element at this index will
            not be included in the calculation of the slot sizes. It will still
            be inserted into the grid at the correct position and may be surrounded
            by padding unless filling the entire line. This is useful for embedding
            decorations in the grid, such as horizontal bars.
        ignore_ansi (bool, optional): Ignore ansi markups when calculating white spacing.
        line_prefix (str, optional): A prefix to add at the beginning of each line.
            This can e.g. be used to preserve line color across line breaks.

    Returns:
        list: The grid as a list of ready-formatted rows. We return it
        like this to make it easier to insert decorations between rows, such
        as horizontal bars.
    """

    def _minimal_rows(elements):
        """
        Minimalistic distribution with minimal spacing, good for single-line
        grids but will look messy over many lines.
        """
        rows = [""]
        for element in elements:
            rowlen = display_len((rows[-1]))
            elen = display_len((element))
            if rowlen + elen <= width:
                rows[-1] += element
            else:
                rows.append(element)
        return rows

    def _weighted_rows(elements):
        """
        Dynamic-space, good for making even columns in a multi-line grid but
        will look strange for a single line.
        """
        wls = [display_len((elem)) for elem in elements]
        wls_percentile = [
            wl for iw, wl in enumerate(wls) if iw not in verbatim_elements
        ]

        if wls_percentile:
            # get the nth percentile as a good representation of average width
            averlen = (
                int(percentile(sorted(wls_percentile), 0.9)) + 2
            )  # include extra space
            aver_per_row = width // averlen + 1
        else:
            # no adjustable rows, just keep all as-is
            aver_per_row = 1

        if aver_per_row == 1:
            # one line per row, output directly since this is trivial
            # we use rstrip here to remove extra spaces added by sep
            return [
                crop(element.rstrip(), width)
                + " " * max(0, width - display_len((element.rstrip())))
                for iel, element in enumerate(elements)
            ]

        indices = [averlen * ind for ind in range(aver_per_row - 1)]

        rows = []
        ic = 0
        row = ""
        for ie, element in enumerate(elements):
            wl = wls[ie]
            lrow = display_len((row))
            # debug = row.replace(" ", ".")

            if lrow + wl > width:
                # this slot extends outside grid, move to next line
                row += " " * (width - lrow)
                rows.append(row)
                if wl >= width:
                    # remove sep if this fills the entire line
                    element = element.rstrip()
                row = crop(element, width)
                ic = 0
            elif ic >= aver_per_row - 1:
                # no more slots available on this line
                row += " " * max(0, (width - lrow))
                rows.append(row)
                row = crop(element, width)
                ic = 0
            else:
                try:
                    while lrow > max(0, indices[ic]):
                        # slot too wide, extend into adjacent slot
                        ic += 1
                    row += " " * max(0, indices[ic] - lrow)
                except IndexError:
                    # we extended past edge of grid, crop or move to next line
                    if ic == 0:
                        row = crop(element, width)
                    else:
                        row += " " * max(0, width - lrow)
                    rows.append(row)
                    row = ""
                    ic = 0
                else:
                    # add a new slot
                    row += element + " " * max(0, averlen - wl)
                    ic += 1

            if ie >= nelements - 1:
                # last element, make sure to store
                row += " " * max(0, width - display_len((row)))
                rows.append(row)
        return rows

    if not elements:
        return []
    if not verbatim_elements:
        verbatim_elements = []

    nelements = len(elements)
    # add sep to all but the very last element
    elements = [elements[ie] + sep for ie in range(nelements - 1)] + [elements[-1]]

    if sum(display_len((element)) for element in elements) <= width:
        # grid fits in one line
        rows = _minimal_rows(elements)
    else:
        # full multi-line grid
        rows = _weighted_rows(elements)

    if line_prefix:
        return [line_prefix + row for row in rows]
    return rows
