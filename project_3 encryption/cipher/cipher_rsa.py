""" RSA module """
from random import randint

from project_3.cipher.cipher import Cipher
from project_3.utils.crypto_utils import generate_random_prime, \
    modular_inverse, blocks_from_text, text_from_blocks


class RSA(Cipher):
    """ RSA class """

    def __init__(self):
        """ Initialize RSA """
        super().__init__()
        self.__bit_size = 8
        self.__block_size = 2
        self._cipher_name = 'RSA'

    def generate_keys(self):
        """
        Generate RSA keys.

        :return: (n, e), (n, d)
        """
        _p = generate_random_prime(self.__bit_size)
        while True:
            _q = generate_random_prime(self.__bit_size)
            if _p != _q:
                break
        _n = _p * _q
        phi = (_p - 1) * (_q - 1)

        while True:
            _e = randint(3, phi - 1)
            _d = modular_inverse(_e, phi)
            if _d != -1:
                break
        return (_n, _e), (_n, _d)

    def encode(self, key: int, plain_message: str):
        """
        Encode the message with RSA encryption.

        :param key: the key used to encode
        :param plain_message: the message to encode
        :return: the encoded message
        """
        self._plain_message = plain_message
        blocks = blocks_from_text(self._plain_message, self.__block_size)
        _c = []
        _n, _e = key
        for block in blocks:
            _c.append(pow(block, _e, _n))
        return _c

    def decode(self, key, encrypted_message: str, log: bool = True,
               no_verify: bool = False):
        """
        Decrypts a RSA encoded message.

        :param key: the key used to decode
        :param encrypted_message: the message to decode
        :param log: print log or not
        :param no_verify: verify decrypted message
        :return: the decrypted message
        """
        self._decrypted_message = ''
        _n, _d = key
        blocks = []
        for block in encrypted_message:
            blocks.append(pow(block, _d, _n))
        self._decrypted_message = text_from_blocks(blocks, self.__bit_size)
        if no_verify:
            return self._decrypted_message
        return self.verify(log)
