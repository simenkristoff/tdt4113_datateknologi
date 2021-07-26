""" Receiver module """
from project_3.person.person import Person


class Receiver(Person):
    """ Receiver class """

    def operate_cipher(self, message: str):
        """
        Pass an encrypted message to a cipher for decryption.

        :param message: the message to decrypt
        :return: decrypted message
        """
        return self._cipher.decode(self.key(), message)
