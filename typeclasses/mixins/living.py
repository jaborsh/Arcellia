from handlers import clothing, cooldowns, traits
from world.characters import genders, races

from evennia.utils import lazy_property


class LivingMixin:
    # Handlers
    @lazy_property
    def clothes(self):
        return clothing.ClothingHandler(self)

    @lazy_property
    def cooldowns(self):
        return cooldowns.CooldownHandler(self)

    @lazy_property
    def stats(self):
        return traits.TraitHandler(self, db_attribute_key="stats")

    @lazy_property
    def traits(self):
        return traits.TraitHandler(self, db_attribute_key="traits")

    # Base Properties
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

    @property
    def wealth(self):
        return self.traits.get("wealth")

    @property
    def weight(self):
        return self.traits.get("weight")

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

    # Methods
    def get_display_things(self, looker, **kwargs):
        clothes = self.clothes.all()
        if not clothes:
            return ""

        output = ["|wClothing:|n"]

        # Use a conditional expression to handle empty 'clothes'
        max_position = (
            max([len(item.position) for item in clothes]) + 8 if clothes else 0
        )

        for item in clothes:
            spaces = " " * (max_position - len(f" <worn {item.position}>"))
            if item.covered_by and looker is not self:
                continue
            line = f"|x<worn {item.position}>|n{spaces} {item.get_display_name(looker)}"
            if item.covered_by:
                line += " |x(hidden)|n"
            output.append(line)

        return "\n ".join(output) + "\n"

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
