import re

from utils.text import _INFLECT

from typeclasses.objects import Object


class Currency(Object):
    @property
    def price(self):
        return self.db.price

    def at_pre_get(self, getter, **kwargs):
        """
        Called by the default `get` command before this object has been
        picked up.

        Args:
            getter (DefaultObject): The object about to get this object.
            **kwargs: Arbitrary, optional arguments for users
                overriding the call (unused by default).

        Returns:
            bool: If the object should be gotten or not.

        Notes:
            If this method returns False/None, the getting is cancelled
            before it is even started.
        """
        if quantity := kwargs.get("quantity", self.db.price):
            if quantity < self.db.price:
                getter.db.wealth += quantity
                self.db.price -= quantity

                getter.location.msg_contents(
                    f"$You() $conj(get) {quantity} {self.get_display_name(getter)}.",
                    from_obj=getter,
                )
                return False
            elif quantity >= self.db.price:
                quantity = self.db.price
                getter.db.wealth += quantity
                getter.location.msg_contents(
                    f"$You() $conj(get) {quantity} {self.get_display_name(getter)}.",
                    from_obj=getter,
                )
                self.delete()
                return False

        return True

    def at_get(self, getter, **kwargs):
        """
        Called by the default `get` command when this object has been
        picked up.

        Args:
            getter (Object): The object getting this object.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call (unused by default).

        Notes:
            This hook cannot stop the pickup from happening. Use
            permissions or the at_pre_get() hook for that.
        """
        pass

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

        Returns:
            tuple: This is a tuple `(str, str)` with the singular and plural forms of the key
                including the count.

        Examples:
            obj.get_numbered_name(3, looker, key="foo") -> ("a foo", "three foos")
        """

        plural_category = "plural_key"
        key = kwargs.get("key", self.display_name)

        # Regular expression for color codes
        color_code_pattern = (
            r"(\|(r|g|y|b|m|c|w|x|R|G|Y|B|M|C|W|X|\d{3}|#[0-9A-Fa-f]{6}))"
        )
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
                    _INFLECT.plural(segment, count) if segment.strip() else segment
                )
                plural_segments.append(plural_segment)

                # Apply singularization to text segment
                if len(singular_segments) == 2:
                    # Special handling when singular_segments has exactly two elements
                    segment = _INFLECT.an(segment) if segment.strip() else segment
                    split_segment = segment.split(" ")
                    singular_segment = (
                        singular_segments[1]
                        + _INFLECT.number_to_words(int(self.price))
                        + " "
                        + " ".join(split_segment[1:])
                    )
                    singular_segments[1] = ""
                else:
                    singular_segment = segment
                singular_segments.append(singular_segment)

        plural = "".join(plural_segments)
        singular = "".join(singular_segments)

        # Alias handling as in the original function
        if not self.aliases.get(plural, category=plural_category):
            self.aliases.clear(category=plural_category)
            self.aliases.add(plural, category=plural_category)
            self.aliases.add(singular, category=plural_category)

        return singular, plural
