from handlers import clothing, equipment, traits
from world.characters import genders, races

from evennia.utils import lazy_property
from evennia.utils.utils import dedent


class LivingMixin:
    def at_object_creation(self):
        self.attributes.add("wealth", 0)
        self.stats.add("strength", "Strength", trait_type="static", base=10)
        self.stats.add("dexterity", "Dexterity", trait_type="static", base=10)
        self.stats.add("constitution", "Constitution", trait_type="static", base=10)
        self.stats.add("intelligence", "Intelligence", trait_type="static", base=10)
        self.stats.add("wisdom", "Wisdom", trait_type="static", base=10)
        self.stats.add("charisma", "Charisma", trait_type="static", base=10)
        self.stats.add("health", "Health", trait_type="gauge", base=100)
        self.stats.add("mana", "Mana", trait_type="gauge", base=100)
        self.stats.add("stamina", "Stamina", trait_type="gauge", base=100)

    @lazy_property
    def clothing(self):
        return clothing.ClothingHandler(
            self, db_attribute_key="clothing", default_data=clothing.CLOTHING_DEFAULTS
        )

    @lazy_property
    def equipment(self):
        return equipment.EquipmentHandler(
            self,
            db_attribute_key="equipment",
            default_data=equipment.EQUIPMENT_DEFAULTS,
        )

    @lazy_property
    def stats(self):
        return traits.TraitHandler(self, db_attribute_key="stats")

    @lazy_property
    def traits(self):
        return traits.TraitHandler(self, db_attribute_key="traits")

    @property
    def combat(self):
        return self.location.combat

    @property
    def gender(self):
        return self.traits.get("gender")

    @gender.setter
    def gender(self, value):
        if isinstance(value, str):
            value = genders.GENDER_MAP.get(value)
        elif isinstance(value, genders.Gender):
            pass
        else:
            raise TypeError("Gender must be a string or a Gender class.")

        self.gender.value = value

    @property
    def race(self):
        return self.traits.get("race")

    @race.setter
    def race(self, value):
        if isinstance(value, str):
            value = races.RACE_MAP.get(value)
        elif isinstance(value, races.Race):
            pass
        else:
            raise TypeError("Race must be a string or a Race class.")

        self.race.value = value

    # Stat Properties
    @property
    def strength(self):
        return self.stats.get("strength")

    @property
    def dexterity(self):
        return self.stats.get("dexterity")

    @property
    def constitution(self):
        return self.stats.get("constitution")

    @property
    def intelligence(self):
        return self.stats.get("intelligence")

    @property
    def wisdom(self):
        return self.stats.get("wisdom")

    @property
    def charisma(self):
        return self.stats.get("charisma")

    @property
    def health(self):
        return self.stats.get("health")

    @property
    def mana(self):
        return self.stats.get("mana")

    @property
    def stamina(self):
        return self.stats.get("stamina")

    @property
    def wealth(self):
        return self.attributes.get("wealth", 0)

    @wealth.setter
    def wealth(self, value):
        self.attributes.add("wealth", value)

    appearance_template = dedent(
        """
        {desc}
        
        {equipment}
        
        {clothing}
        """
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
            looker (Object): Object doing the looking. Passed into all helper methods.
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

        return self.appearance_template.format(
            desc=self.get_display_desc(looker, **kwargs),
            equipment=self.get_display_equipment(looker, **kwargs),
            clothing=self.get_display_clothing(looker, **kwargs),
        ).strip()

    def get_display_desc(self, looker, **kwargs):
        """
        Get the 'desc' component of the object description. Called by `return_appearance`.

        Args:
            looker (DefaultObject): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The desc display string.

        """
        return self.db.desc or "You see nothing special."

    def get_display_equipment(self, looker, **kwargs):
        def _filter_visible(obj_list):
            return [
                obj for obj in obj_list if obj != looker and obj.access(looker, "view")
            ]

        equipment = _filter_visible(self.equipment.all())
        if not equipment:
            return ""

        string = "|wEquipment:|n"
        max_position = (
            max([len(item.position) for item in equipment]) + 8 if equipment else 0
        )

        for item in equipment:
            spaces = " " * (max_position - len(f" <worn {item.position}>"))
            line = f" |x<{item.position}>|n{spaces} {item.get_display_name(looker)}"
            string += f"\n{line}"

        return string

    def get_display_clothing(self, looker, **kwargs):
        def _filter_visible(obj_list):
            return [
                obj for obj in obj_list if obj != looker and obj.access(looker, "view")
            ]

        clothing = _filter_visible(self.clothing.all())
        if not clothing:
            return ""

        string = "|wClothing:|n"
        max_position = (
            max([len(item.position) for item in clothing]) + 8 if clothing else 0
        )

        for item in clothing:
            spaces = " " * (max_position - len(f" <worn {item.position}>"))
            if item.covered_by and looker is not self:
                continue

            line = (
                f" |x<worn {item.position}>|n{spaces} {item.get_display_name(looker)}"
            )
            if item.covered_by:
                line += " |x(hidden)|n"
            string += f"\n{line}"

        return string

    def get_pronoun(self, regex_match):
        """
        Get pronoun from the pronoun marker in the text. This is used as
        the callable for the re.sub function.

        Args:
            regex_match (MatchObject): the regular expression match.

        Notes:
            - `|s`, `|S`: Subjective form: he, she, it, He, She, It, They
            - `|o`, `|O`: Objective form: him, her, it, Him, Her, It, Them
            - `|p`, `|P`: Possessive form: his, her, its, His, Her, Its, Their
            - `|a`, `|A`: Absolute Possessive form: his, hers, its, His, Hers, Its, Theirs

        """  # noqa: E501
        typ = regex_match.group()[1]  # "s", "O" etc
        gender = self.gender
        pronoun = genders._GENDER_PRONOUN_MAP[gender][typ.lower()]
        return pronoun.capitalize() if typ.isupper() else pronoun
