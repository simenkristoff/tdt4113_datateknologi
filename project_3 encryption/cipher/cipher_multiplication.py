""" Multiplication module """
from random import randint

from project_3.cipher.cipher_alpha import AlphaCipher
from project_3.utils.crypto_utils import modular_inverse


class Multiplication(AlphaCipher):
    """ Multiplication class """

    def __init__(self):
        """ Initialize Multiplication """
        super().__init__()
        self._cipher_name = 'Multiplication'

    def generate_keys(self):
        """
        Generate keys.

        :return: key, key
        """
        while True:
            key = randint(0, self._alphabet_size)
            if modular_inverse(key, self._alphabet_size) != -1:
                return key, key

    def encode(self, key: int, plain_message: str):
        """
        Encode the message with Multiplication encryption.

        :param key: the key used to encode
        :param plain_message: the message to encode
        :return: the encoded message
        """
        self._plain_message = plain_message
        encrypted_message = ''
        for _c in self._plain_message:
            encrypted_message += self._alphabet[(
                self._alphabet[_c] * key) % self._alphabet_size]
        return encrypted_message

    def decode(self, key, encrypted_message: str, log: bool = True,
               no_verify: bool = False):
        """
        Decrypts a Multiplication encoded message.

        :param key: the key used to decode
        :param encrypted_message: the message to decode
        :param log: print log or not
        :param no_verify: verify decrypted message
        :return: the decrypted message
        """
        self._decrypted_message = ''
        inverse_key = modular_inverse(key, self._alphabet_size)
        for _c in encrypted_message:
            self._decrypted_message += self._alphabet[(
                self._alphabet[_c] * inverse_key) % self._alphabet_size]
        if no_verify:
            return self._decrypted_message
        return self.verify(log)
