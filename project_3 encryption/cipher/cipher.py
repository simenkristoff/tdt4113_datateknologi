""" Cipher module """


class Cipher:
    """ Cipher class """

    def __init__(self):
        """
        Initializes the Cipher.
        """
        self._cipher_name = ''
        self._plain_message = ''
        self._decrypted_message = ''

    def generate_keys(self):
        """
        Generates keys for the specified cipher.

        :return: keys
        """
        raise NotImplementedError('generate_keys not yet implemented')

    def encode(self, key, plain_message: str):
        """
        Encrypts a message.

        :param key: the key used to encrypt
        :param plain_message: the message to encrypt
        :raises: NotImplementedError
        """
        raise NotImplementedError('encode not yet implemented')

    def decode(self, key, encrypted_message: str, log: bool = True,
               no_verify: bool = False):
        """
        Decrypts a message.

        :param key: the key used to decrypt
        :param encrypted_message: the message to decrypt
        :param log: print log or not
        :param no_verify: verify decrypted message
        :raises: NotImplementedError
        """
        raise NotImplementedError('decode not yet implemented')

    def verify(self, log: bool):
        """
        Verify if the cipher has decrypted the message correctly.

        :param log: print log or not
        :raises: ValueError
        :return: the decrypted message
        """

        if self._plain_message == self._decrypted_message:
            if log:
                print(f'[PLAIN MESSAGE]: {self._plain_message}\n'
                      f'[DECRYPTED MESSAGE]: {self._decrypted_message}\n'
                      f'[SUCCESS]: {self._cipher_name} verified')
            return self._decrypted_message
        raise ValueError(f'[FAILURE]: {self._cipher_name} Encryption Invalid')

    def get_name(self):
        """
        Returns the name of the cipher.

        :return: the cipher name
        """
        return self._cipher_name
