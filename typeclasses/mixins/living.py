from evennia.contrib.rpg.traits import traits
from evennia.utils import lazy_property
from handlers import clothing, cooldowns
from world.base import genders


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

    # Base Properties
    @property
    def display_name(self):
        return self.base.get("display_name") or self.name

    @property
    def gender(self):
        return self.base.get("gender") or genders.Gender.ANDROGYNOUS

    # Stat Properties
    @property
    def strength(self):
        return self.stats.get("strength") or 10

    @property
    def dexterity(self):
        return self.stats.get("dexterity") or 10

    @property
    def constitution(self):
        return self.stats.get("constitution") or 10

    @property
    def intelligence(self):
        return self.stats.get("intelligence") or 10

    @property
    def wisdom(self):
        return self.stats.get("wisdom") or 10

    @property
    def charisma(self):
        return self.stats.get("charisma") or 10

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
