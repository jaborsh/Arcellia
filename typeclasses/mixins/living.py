from evennia.utils import lazy_property
from handlers import traits
from world.characters import genders, races


class LivingMixin:
    @lazy_property
    def traits(self):
        return traits.TraitHandler(self, db_attribute_key="traits")

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
