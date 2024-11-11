from collections import defaultdict

from evennia.utils import dbserialize
from evennia.utils.utils import compress_whitespace, iter_to_str

from utils.text import (
    _INFLECT,
    extract_color_codes,
    extract_id_suffix,
    reapply_color_codes,
)

APPEARANCE_TEMPLATE = "{desc}\n\n{characters}\n{things}"


class AppearanceHandler:
    """
    Handles the appearance and description systems for game objects.

    This handler manages how objects appear to others in the game, including their
    descriptions, details, and sensory information. It provides methods for storing,
    retrieving, and displaying object appearances.

    Attributes:
        obj (Object): The game object this handler is attached to
        descriptions (dict): Stored descriptions for the object
        details (dict): Stored details for examining specific parts of the object
        senses (dict): Stored sensory information for non-visual perceptions
    """

    def __init__(self, obj, db_attribute_key="appearance", db_category=None):
        """
        Initialize the AppearanceHandler.

        Args:
            obj (Object): The game object this handler belongs to
            db_attribute_key (str, optional): Database attribute key for storing appearance data.
                Defaults to "appearance".
            db_category (str, optional): Database category for the appearance attribute.
                Defaults to None.
        """
        self.obj = obj
        self._db_attribute = db_attribute_key
        self._db_category = db_category
        self.descriptions = {}
        self.details = {}
        self.senses = {}
        self._load()

    def _load(self):
        """
        Load appearance data from the database.

        Retrieves and deserializes stored descriptions, details, and sensory data
        from the object's attributes.
        """
        if data := self.obj.attributes.get(
            self._db_attribute, category=self._db_category
        ):
            self.descriptions = dbserialize.deserialize(
                data.get("descriptions", {})
            )
            self.details = dbserialize.deserialize(data.get("details", {}))
            self.senses = dbserialize.deserialize(data.get("senses", {}))

    def _save(self):
        """
        Save appearance data to the database.

        Serializes and stores the current descriptions, details, and sensory data
        to the object's attributes.
        """
        self.obj.attributes.add(
            self._db_attribute,
            {
                "descriptions": self.descriptions,
                "details": self.details,
                "senses": self.senses,
            },
            category=self._db_category,
        )

    def _filter_visible(self, looker, obj_list):
        """
        Filter a list of objects to only those visible to the looker.

        Args:
            looker (Object): The object doing the looking
            obj_list (list): List of objects to filter

        Returns:
            list: Objects that are visible to the looker
        """
        return [
            obj
            for obj in obj_list
            if obj != looker and obj.access(looker, "view")
        ]

    def get_display_name(self, looker=None, **kwargs):
        """
        Get the display name of the object for a specific looker.

        Args:
            looker (Object, optional): The object doing the looking
            **kwargs: Additional parameters for customizing the display

        Returns:
            str: The formatted display name, optionally including the object ID for builders

        Notes:
            - Returns object ID (#xxx) suffix for users with Builder permissions
            - Can be extended to provide different names based on the looker's properties
        """
        if looker and self.obj.locks.check_lockstring(looker, "perm(Builder)"):
            return f"{self.obj.display_name}(#{self.obj.id})"
        return self.obj.display_name

    def get_display_desc(self, looker, **kwargs):
        """
        Get the main description of the object.

        Args:
            looker (Object): The object doing the looking
            **kwargs: Additional parameters for customizing the description

        Returns:
            str: The formatted description text

        Notes:
            - Returns a default message if no description is set
            - Description is stripped of leading/trailing whitespace
        """
        return self.descriptions.get("default", "You see nothing special.")

    def get_display_characters(self, looker, **kwargs):
        """
        Get a formatted list of characters present in the object's location.

        Args:
            looker (Object): The object doing the looking
            **kwargs: Additional parameters for customizing character display

        Returns:
            str: Formatted string listing visible characters, or empty string if none

        Notes:
            - Excludes the looker from the character list
            - Only shows characters the looker has permission to see
            - Returns an empty string if no visible characters are present
        """
        characters = self._filter_visible(
            looker, self.obj.contents_get(content_type="character")
        )
        if not characters:
            return ""
        character_names = iter_to_str(
            char.get_display_name(looker, **kwargs) for char in characters
        )
        return f"|wCharacters:|n {character_names}"

    def get_display_things(self, looker=None, **kwargs):
        """
        Get a formatted list of non-character objects in the location.

        Args:
            looker (Object, optional): The object doing the looking
            **kwargs: Additional parameters for customizing object display

        Returns:
            str: Formatted string listing visible objects, or empty string if none

        Notes:
            - Groups identical objects together with appropriate pluralization
            - Only shows objects the looker has permission to see
            - Objects are sorted alphabetically
        """
        things = self._filter_visible(
            looker, self.obj.contents_get(content_type="object")
        )
        if not things:
            return ""

        grouped_things = defaultdict(list)
        for thing in things:
            grouped_things[thing.get_display_name(looker, **kwargs)].append(
                thing
            )

        thing_strings = []
        for thingname, thinglist in sorted(grouped_things.items()):
            thing = thinglist[0]
            nthings = len(thinglist)
            singular, plural = thing.get_numbered_name(
                nthings, looker, key=thingname
            )
            thing_strings.append(singular if nthings == 1 else plural)

        return "|wYou see:|n" + "\n " + "\n ".join(thing_strings)

    def get_numbered_name(self, count, looker, **kwargs):
        """
        Get the singular and plural forms of an object's name with proper articles.

        Args:
            count (int): Number of objects being described
            looker (Object): The object doing the looking
            **kwargs: Additional customization parameters:
                - key (str): Optional specific key to pluralize
                - return_string (bool): If True, return only one form based on count
                - no_article (bool): If True, omit articles for singular forms

        Returns:
            tuple or str: Either (singular_form, plural_form) tuple or a single string

        Notes:
            - Handles special cases like "pairs of X"
            - Preserves color codes in the formatted string
            - Can override the base key via the 'key' kwarg
        """
        key = kwargs.get("key", self.obj.get_display_name(looker))
        key, id_suffix = extract_id_suffix(key)
        clean_key, colors = extract_color_codes(key)
        no_article = kwargs.get("no_article", False)

        is_pair = bool(_INFLECT.singular_noun(clean_key))

        if is_pair:
            clean_singular = clean_key
            prefix = f"{_INFLECT.number_to_words(count)} pairs of "
            clean_plural = prefix + clean_key
        else:
            clean_singular = (
                _INFLECT.an(clean_key) if not no_article else clean_key
            )
            prefix = f"{_INFLECT.number_to_words(count)} "
            clean_plural = prefix + _INFLECT.plural(clean_key, count)

        singular = (
            reapply_color_codes(
                clean_singular, colors, len(clean_singular) - len(clean_key)
            )
            + id_suffix
        )
        plural = (
            reapply_color_codes(clean_plural, colors, len(prefix)) + id_suffix
        )

        return (
            (singular, plural)
            if not kwargs.get("return_string")
            else (singular if count == 1 else plural)
        )

    def return_appearance(self, looker, **kwargs):
        """
        Generate a complete description of the object for a looker.

        This is the main method called by the 'look' command to get an object's
        full description.

        Args:
            looker (Object): The object doing the looking
            **kwargs: Additional parameters for customizing the appearance

        Returns:
            str: Complete formatted description including name, description,
                characters present, and visible objects

        Notes:
            - Uses APPEARANCE_TEMPLATE to format the final output
            - Combines results from get_display_desc, get_display_characters,
              and get_display_things
            - Strips excessive whitespace and normalizes line breaks
            - Returns empty string if no looker is provided
        """
        if not looker:
            return ""

        return compress_whitespace(
            APPEARANCE_TEMPLATE.format(
                desc=self.get_display_desc(looker, **kwargs),
                characters=self.get_display_characters(looker, **kwargs),
                things=self.get_display_things(looker, **kwargs),
            ).strip(),
            max_linebreaks=2,
        )
