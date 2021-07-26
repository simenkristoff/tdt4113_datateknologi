""" AlphaCipher module """
from project_3.cipher.cipher import Cipher
from project_3.utils.utils import create_alphabet


class AlphaCipher(Cipher):
    """
    AlphaCipher class wrapper for Ciphers using alphabet
    for encryption/decryption
    """

    def __init__(self):
        """
        Initializes the Alpha Cipher.
        """
        super().__init__()
        self._alphabet = create_alphabet()
        self._alphabet_size = len(self._alphabet) // 2

    def generate_keys(self):
        pass

    def encode(self, key, plain_message: str):
        pass

    def decode(self, key, encrypted_message: str, log: bool = True,
               no_verify: bool = False):
        pass

    @property
    def alphabet_size(self):
        """
        Get the alphabet size.

        :return: the alphabet size
        """
        return self._alphabet_size
