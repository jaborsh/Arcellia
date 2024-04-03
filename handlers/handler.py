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

    __slots__ = ("data", "db_attribute", "obj")

    def __init__(self, obj, db_attribute):
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
        if not obj.attributes.get(db_attribute, None):
            obj.attributes.add(db_attribute, {})

        self.data = obj.attributes.get(db_attribute)
        self.obj = obj
        self.db_attribute = db_attribute

    def _load(self):
        """
        Loads the data from the object's attributes dictionary.

        This method retrieves the data associated with the attribute from the object's attributes dictionary and assigns it to the 'data' attribute of the Handler object.

        Parameters:
            None

        Returns:
            None

        Raises:
            None
        """
        self.data = self.obj.attributes.get(self.db_attribute, default={})

    def _save(self):
        """
        Saves the data to the object's attributes dictionary.

        This method saves the data associated with the attribute to the object's attributes dictionary. It uses the 'add' method of the 'attributes' object to add the data with the specified attribute name. After saving the data, it calls the '_load' method to update the 'data' attribute of the Handler object.

        Parameters:
            None

        Returns:
            None

        Raises:
            None
        """
        self.obj.attributes.add(self.db_attribute, self.data)
        self._load()

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
        return self.data

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
        return self.data.get(key, None)
