class MailHandler:
    """
    Handler for mail. This is attached to any object that supports mail as a
    feature (Characters and Accounts).
    """

    def __init__(self, owner, db_attribute="mail"):
        """
        Initialize the mail handler with the owner and an empty inbox.
        """

        if not owner.attributes.has(db_attribute):
            owner.attributes.add(db_attribute, [])

        self.owner = owner
        self.inbox = owner.attributes.get(db_attribute)

    def view_mail(self):
        """
        View the contents of the owner's mailbox.
        """
        return self.inbox

    def delete_mail(self, index):
        """
        Delete a letter from the inbox.

        Args:
            index (int): The index of the letter to delete

        Returns:
            str: Confirmation message
        """

        index -= 1
        if 0 <= index < len(self.inbox):
            del self.inbox[index]
            return "Letter deleted."

        return "Invalid letter."
