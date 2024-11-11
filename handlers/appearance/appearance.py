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
    def __init__(self, obj, db_attribute_key="appearance", db_category=None):
        self.obj = obj
        self._db_attribute = db_attribute_key
        self._db_category = db_category
        self.descriptions = {}
        self.details = {}
        self.senses = {}
        self._load()

    def _load(self):
        if data := self.obj.attributes.get(
            self._db_attribute, category=self._db_category
        ):
            self.descriptions = dbserialize.deserialize(
                data.get("descriptions", {})
            )
            self.details = dbserialize.deserialize(data.get("details", {}))
            self.senses = dbserialize.deserialize(data.get("senses", {}))

    def _save(self):
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
        return [
            obj
            for obj in obj_list
            if obj != looker and obj.access(looker, "view")
        ]

    def get_display_name(self, looker=None, **kwargs):
        """
        Displays the name of the object in a viewer-aware manner.

        Args:
            looker (DefaultObject): The object or account that is looking at or getting information
                for this object.

        Returns:
            str: A name to display for this object. By default this returns the `.name` of the object.

        Notes:
            This function can be extended to change how object names appear to users in character,
            but it does not change an object's keys or aliases when searching.
        """
        if looker and self.obj.locks.check_lockstring(looker, "perm(Builder)"):
            return f"{self.obj.display_name}(#{self.obj.id})"
        return self.obj.display_name

    def get_display_desc(self, looker, **kwargs):
        """
        Get the 'desc' component of the object description. Called by `return_appearance`.

        Args:
            looker (DefaultObject): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The desc display string.

        """
        return self.obj.db.desc.strip() or "You see nothing special."

    def get_display_characters(self, looker, **kwargs):
        """
        Get the 'characters' component of the object description. Called by `return_appearance`.

        Args:
            looker (DefaultObject): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The character display data.

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
        Get the 'things' component of the object description. Called by `return_appearance`.

        Args:
            looker (DefaultObject): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The things display data.
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
        Return the numbered (singular, plural) forms of this object's key. This is by default called
        by return_appearance and is used for grouping multiple same-named of this object. Note that
        this will be called on *every* member of a group even though the plural name will be only
        shown once. Also the singular display version, such as 'an apple', 'a tree' is determined
        from this method.

        Args:
            count (int): Number of objects of this type
            looker (DefaultObject): Onlooker. Not used by default.

        Keyword Args:
            key (str): Optional key to pluralize. If not given, the object's `.get_display_name()`
                method is used.
            return_string (bool): If `True`, return only the singular form if count is 0,1 or
                the plural form otherwise. If `False` (default), return both forms as a tuple.
            no_article (bool): If `True`, do not return an article if `count` is 1.

        Returns:
            tuple: This is a tuple `(str, str)` with the singular and plural forms of the key
            including the count.

        Examples:
        ::

            obj.get_numbered_name(3, looker, key="foo")
                  -> ("a foo", "three foos")
            obj.get_numbered_name(1, looker, key="Foobert", return_string=True)
                  -> "a Foobert"
            obj.get_numbered_name(1, looker, key="Foobert", return_string=True, no_article=True)
                  -> "Foobert"
        """
        key = kwargs.get("key", self.obj.get_display_name(looker))
        key, id_suffix = extract_id_suffix(key)
        clean_key, colors = extract_color_codes(key)

        is_pair = bool(_INFLECT.singular_noun(clean_key))

        if is_pair:
            clean_singular = clean_key
            prefix = f"{_INFLECT.number_to_words(count)} pairs of "
            clean_plural = prefix + clean_key
        else:
            clean_singular = _INFLECT.an(clean_key)
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

        if kwargs.get("no_article") and count == 1:
            return (
                (singular, plural) if not kwargs.get("return_string") else key
            )

        return (
            (singular, plural)
            if not kwargs.get("return_string")
            else (singular if count == 1 else plural)
        )

    def return_appearance(self, looker, **kwargs):
        """
        Main callback used by 'look' for the object to describe itself.
        This formats a description. By default, this looks for the `appearance_template`
        string set on this class and populates it with formatting keys
        'name', 'desc', 'exits', 'characters', 'things' as well as
        (currently empty) 'header'/'footer'. Each of these values are
        retrieved by a matching method `.get_display_*`, such as `get_display_name`,
        `get_display_footer` etc.

        Args:
            looker (DefaultObject): Object doing the looking. Passed into all helper methods.
            **kwargs (dict): Arbitrary, optional arguments for users
                overriding the call. This is passed into all helper methods.

        Returns:
            str: The description of this entity. By default this includes
            the entity's name, description and any contents inside it.

        Notes:
            To simply change the layout of how the object displays itself (like
            adding some line decorations or change colors of different sections),
            you can simply edit `.appearance_template`. You only need to override
            this method (and/or its helpers) if you want to change what is passed
            into the template or want the most control over output.

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
