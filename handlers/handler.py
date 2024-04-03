from copy import copy

from evennia.utils import dbserialize


class Handler:
    """
    A class that handles data for a specific attribute of an object.

    Attributes:
        data (dict): The data associated with the attribute.
        db_attribute (str): The name of the attribute in the object's attributes dictionary.
        obj (object): The object for which the data is being handled.

    Methods:
        __init__(self, obj, db_attribute): Initializes the Handler object.
        _load(self): Loads the data from the object's attributes dictionary.
        _save(self): Saves the data to the object's attributes dictionary.
        all(self): Returns all the data associated with the attribute.
        get(self, key): Returns the value associated with the given key in the data dictionary.
    """

    def __init__(
        self, obj, db_attribute_key, db_attribute_category=None, default_data={}
    ):
        """
        Initializes a Handler object.

        Parameters:
            obj (object): The object for which the data is being handled.
            db_attribute (str): The name of the attribute in the object's attributes dictionary.

        Attributes:
            data (dict): The data associated with the attribute.
            db_attribute (str): The name of the attribute in the object's attributes dictionary.
            obj (object): The object for which the data is being handled.
        """
        self.obj = obj
        self._db_attr = db_attribute_key
        self._db_cat = db_attribute_category
        self._data = copy(default_data)
        self._load()

    def _load(self):
        if data := self.obj.attributes.get(self._db_attr, category=self._db_cat):
            self._data = dbserialize.deserialize(data)

    def _save(self):
        self.obj.attributes.add(self._db_attr, self._data, category=self._db_cat)

    def all(self):
        """
        Returns all the data associated with the attribute.

        Parameters:
            None

        Returns:
            dict: The data associated with the attribute.

        Raises:
            None
        """
        return self._data

    def get(self, key):
        """
        Returns the value associated with the given key in the data dictionary.

        Parameters:
            key (hashable): The key to retrieve the value for.

        Returns:
            Any: The value associated with the given key, or None if the key is not found.

        Raises:
            None
        """
        return self._data.get(key, None)
