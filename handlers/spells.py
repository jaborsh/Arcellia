from copy import copy

from evennia.utils.utils import inherits_from

from commands.spells import evocation, necromancy, spells

from .handler import Handler

_SPELLS = evocation.EVOCATION_SPELL_DATA | necromancy.NECROMANCY_SPELL_DATA


class SpellHandler(Handler):
    """
    A class that handles spells.

    Attributes:
        _data (dict): A dictionary that stores spell data.

    Methods:
        all(): Returns a list of all spells in the handler.
        get(spell_key): Retrieves a spell from the handler.
        add(spell_key, spell_cls): Adds a spell to the handler.
        remove(spell_key): Removes a spell from the handler.
    """

    def __init__(
        self, obj, db_attribute_key, db_attribute_category=None, default_data=[]
    ):
        """
        Initializes a Handler object.

        Parameters:
            obj (object): The object for which the data is being handled.
            db_attribute (str): The name of the attribute in the object's attributes dictionary.

        Attributes:
            data (list): The list associated with the attribute.
            db_attribute (str): The name of the attribute in the object's attributes dictionary.
            obj (object): The object for which the data is being handled.
        """
        self.obj = obj
        self._db_attr = db_attribute_key
        self._db_cat = db_attribute_category
        self._data = copy(default_data)
        self._load()

    def all(self):
        """
        Returns a list of all spells in the handler.

        Returns:
            list: A list of all spells in the handler.
        """
        return self._data

    def get(self, spell_key):
        """
        Retrieves a spell from the handler.

        Args:
            spell_key (str): The key of the spell to retrieve.

        Returns:
            Spell: The retrieved spell.
        """
        return _SPELLS.get(spell_key) if spell_key in self._data else None

    def add(self, spell):
        """
        Adds a spell to the handler.

        Args:
            spell (str or Spell): The key of the spell or the spell class.
        """

        if isinstance(spell, str) and _SPELLS.get(spell) is not None:
            self._data.append(spell)
        elif inherits_from(spell, spells.Spell):
            self._data.append(spell.key)
        else:
            raise ValueError("Invalid spell.")

        self._save()

    learn = add  # Alias for add

    def remove(self, spell_key):
        """
        Removes a spell from the handler.

        Args:
            spell_key (str): The key of the spell to remove.
        """
        self._data.remove(spell_key)
        self._save()

    def cast(self, spell_key, target=None):
        """
        Casts a spell.

        Args:
            spell_key (str): The key of the spell to cast.
            target (object, optional): The target of the spell. Defaults to None.
        """
        spell = _SPELLS.get(spell_key)
        if spell:
            spell.cast(self.obj, target=target)
        else:
            self.obj.msg("You don't know that spell.")

    def clear(self):
        """
        Clears all spells from the handler.
        """
        self._data = []
        self._save()
