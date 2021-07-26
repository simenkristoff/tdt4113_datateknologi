""" Caesar module """
from random import randint

from project_3.cipher.cipher_alpha import AlphaCipher


class Caesar(AlphaCipher):
    """ Caesar class """

    def __init__(self):
        """ Initialize Caesar """
        super().__init__()
        self._cipher_name = 'Caesar'

    def generate_keys(self):
        """
        Generate keys.

        :return: key, key
        """
        key = randint(0, self._alphabet_size)
        return key, key

    def encode(self, key: int, plain_message: str):
        """
        Encode the message with Caesar encryption.

        :param key: the key used to encode
        :param plain_message: the message to encode
        :return: the encoded message
        """
        self._plain_message = plain_message
        encrypted_message = ''
        for _c in self._plain_message:
            encrypted_message += self._alphabet[(
                self._alphabet[_c] + key) % self._alphabet_size]
        return encrypted_message

    def decode(self, key, encrypted_message: str, log: bool = True,
               no_verify: bool = False):
        """
        Decrypts a Caesar encoded message.

        :param key: the key used to decode
        :param encrypted_message: the message to decode
        :param log: print log or not
        :param no_verify: verify decrypted message
        :return: the decrypted message
        """
        self._decrypted_message = ''
        for _c in encrypted_message:
            self._decrypted_message += self._alphabet[(
                self._alphabet[_c] - key) % self._alphabet_size]
        if no_verify:
            return self._decrypted_message
        return self.verify(log)
