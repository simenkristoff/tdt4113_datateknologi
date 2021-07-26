""" Sender module """
from project_3.person.person import Person


class Sender(Person):
    """ Sender class """

    def operate_cipher(self, message: str):
        """
        Pass the message to a cipher for encryption.

        :param message: the message to encrypt
        :return: encrypted message
        """
        return self._cipher.encode(self.key(), message)
