""" Person module """
from project_3.cipher.cipher import Cipher


# noinspection PyAttributeOutsideInit
class Person:
    """ Person class """

    def __init__(self, cipher: Cipher):
        """
        Initializes Person instance.

        :param cipher: the cipher to be used
        """
        self._cipher = cipher

    def key(self):
        """
        Returns the key.

        :return: key
        """
        return self._key

    def set_key(self, key):
        """
        Sets the persons key.

        :param key: the key to set
        """
        self._key = key

    def operate_cipher(self, message):
        """
        Operate the cipher.

        :param message: the message to cipher
        :raises: NotImplementedError
        """
        raise NotImplementedError('operate_cipher not yet implemented')
