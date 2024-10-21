import random
import re

from evennia.utils.utils import lazy_property

from typeclasses.objects import Object
from utils.text import _INFLECT, strip_ansi


class Book(Object):
    @lazy_property
    def stories(self):
        return self.attributes.get("stories", [])

    def at_read(self, reader):
        if not self.stories:
            return reader.msg("The book is empty.")

        if len(self.stories) == 1:
            return reader.msg(self.stories[0])

        reader.msg(random.choice(self.stories))

    def get_numbered_name(self, count, looker, **kwargs):
        """
        Return the numbered (singular, plural) forms of this object's key. This
        is by default called by return_appearance and is used for grouping
        multiple same-named of this object. Note that this will be called on
        *every* member of a group even though the plural name will be only shown
        once. Also the singular display version, such as 'an apple', 'a tree'
        is determined from this method.

        Args:
            count (int): Number of objects of this type
            looker (Object): Onlooker. Not used by default.

        Keyword Args:
            key (str): Optional key to pluralize. If not given, the object's `.name` property is
                used.
            no_article (bool): If 'True', do not return an article if 'count' is 1.

        Returns:
            tuple: This is a tuple `(str, str)` with the singular and plural forms of the key
                including the count.

        Examples:
            obj.get_numbered_name(3, looker, key="foo") -> ("a foo", "three foos")
        """

        if count == 1:
            return self.get_display_name(
                looker
            ) + self.get_extra_display_name_info(looker), self.get_display_name(
                looker
            ) + self.get_extra_display_name_info(looker)

        key = kwargs.get("key", self.get_display_name(looker))
        # Regular expression for color codes
        color_code_pattern = r"(\|(r|g|y|b|m|c|w|x|R|G|Y|B|M|C|W|X|\d{3}|#[0-9A-Fa-f]{6})|\[.*\])"
        color_code_positions = [
            (m.start(0), m.end(0)) for m in re.finditer(color_code_pattern, key)
        ]

        # Split the key into segments of text and color codes
        segments = []
        last_pos = 0
        for start, end in color_code_positions:
            segments.append(key[last_pos:start])  # Text segment
            segments.append(key[start:end])  # Color code
            last_pos = end
        segments.append(key[last_pos:])  # Remaining text after last color code

        # Apply pluralization and singularization to each text segment
        plural_segments = []
        singular_segments = []
        for segment in segments:
            if re.match(color_code_pattern, segment):
                # Color code remains unchanged for both plural and singular segments
                plural_segments.append(segment)
                singular_segments.append(segment)
            else:
                # Apply pluralization to text segment
                plural_segment = (
                    _INFLECT.plural(segment, count)
                    if segment.strip()
                    else segment
                )
                plural_segments.append(plural_segment)

                # Apply singularization to text segment
                if len(singular_segments) == 2:
                    # Special handling when singular_segments has exactly two elements
                    segment = (
                        _INFLECT.an(segment) if segment.strip() else segment
                    )
                    split_segment = segment.split(" ")
                    singular_segment = (
                        strip_ansi(split_segment[0])
                        + singular_segments[1]
                        + " "
                        + " ".join(split_segment[1:])
                    )
                    singular_segments[1] = ""
                else:
                    singular_segment = segment
                singular_segments.append(singular_segment)

        plural = re.split(color_code_pattern, "".join(plural_segments), 1)
        plural = (
            _INFLECT.number_to_words(count)
            + " "
            + plural[1]
            + _INFLECT.plural(plural[3], count)
            + "|n"
            if len(plural) > 1
            else _INFLECT.plural(plural[0])
        )
        singular = "".join(singular_segments)

        # Alias handling as in the original function
        if not self.aliases.get(strip_ansi(singular)):
            self.aliases.add(strip_ansi(singular))
        if not self.aliases.get(strip_ansi(plural)):
            self.aliases.add(strip_ansi(plural))

        return singular, plural
