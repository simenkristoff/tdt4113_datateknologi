""" Affine module """
from project_3.cipher.cipher_alpha import AlphaCipher
from project_3.cipher.cipher_caesar import Caesar
from project_3.cipher.cipher_multiplication import Multiplication


class Affine(AlphaCipher):
    """ Affine class """

    def __init__(self):
        """ Initialize Affine """
        super().__init__()
        self._cipher_name = 'Affine'
        self.__caesar = Caesar()
        self.__multiplication = Multiplication()

    def generate_keys(self):
        """
        Generate keys.

        :return: (multi_key, caesar_key), (multi_key, caesar_key)
        """
        c_key = self.__caesar.generate_keys()[0]
        m_key = self.__multiplication.generate_keys()[0]
        return (m_key, c_key), (m_key, c_key)

    def encode(self, key: int, plain_message: str):
        """
        Encode the message with Affine encryption.

        :param key: the key used to encode
        :param plain_message: the message to encode
        :return: the encoded message
        """
        m_key, c_key = key
        self._plain_message = plain_message
        encrypted_message = self.__multiplication.encode(
            m_key, self._plain_message)
        return self.__caesar.encode(c_key, encrypted_message)

    def decode(self, key, encrypted_message: str, log: bool = True,
               no_verify: bool = False):
        """
        Decrypts an Affine encoded message.

        :param key: the key used to decode
        :param encrypted_message: the message to decode
        :param log: print log or not
        :param no_verify: verify decrypted message
        :return: the decrypted message
        """
        self._decrypted_message = ''
        m_key, c_key = key
        dec_msg = self.__caesar.decode(c_key, encrypted_message, False, True)
        self._decrypted_message = self.__multiplication.decode(
            m_key, dec_msg, False, True)
        if no_verify:
            return self._decrypted_message
        return self.verify(log)
