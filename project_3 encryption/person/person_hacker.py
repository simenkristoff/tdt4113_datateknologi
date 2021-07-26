""" Hacker module """
from project_3.cipher.cipher import Cipher
from project_3.cipher.cipher_affine import Affine
from project_3.cipher.cipher_caesar import Caesar
from project_3.cipher.cipher_multiplication import Multiplication
from project_3.cipher.cipher_unbreakable import Unbreakable
from project_3.person.person import Person
from project_3.utils.crypto_utils import modular_inverse
from project_3.utils.utils import load_dictionary


class Hacker(Person):
    """ Hacker class """
    ITERATIONS = 10
    THRESHOLD = 0.4

    def __init__(self, cipher: Cipher = None):
        """ Initialize Hacker """
        super().__init__(cipher)
        self.dictionary = load_dictionary()
        self._decrypted_message = ''

    def _verify_text(self, decrypted_message):
        """
        Verifies the decrypted message. If the message is a long word,
        it's probably not a decrypted text.

        :param decrypted_message: the message to verify
        :return: boolean
        """
        words = decrypted_message.split(" ")
        if len(decrypted_message) / len(words) >= 12:
            return False

        word_matches = 0
        for word in words:
            if self.dictionary.get(word.lower()):
                word_matches += 1
        return True if word_matches / len(words) > self.THRESHOLD else False

    def _is_verified(self):
        """
        Checks if the message is verified, i.e. not None.

        :return: boolean, True if verified
        """
        if self._decrypted_message:
            print(f'[SUCCESS]: The encrypted message was hacked!\n'
                  f'=> {self._decrypted_message}')
            return True
        print('[FAILURE]: Decryption failed')
        return False

    def _decrypt_caesar(self, encrypted_message):
        """
        Try to brute force Caesar encryption

        :param encrypted_message: the message to decrypt
        :return: decrypted message | None
        """
        caesar = Caesar()
        for i in range(caesar.alphabet_size * self.ITERATIONS):
            message = caesar.decode(i, encrypted_message, False, True)
            if self._verify_text(message):
                return message
        return None

    def _decrypt_multiplication(self, encrypted_message):
        """
        Try to brute force Multiplication encryption

        :param encrypted_message: the message to decrypt
        :return: decrypted message | None
        """
        multiplication = Multiplication()
        for i in range(multiplication.alphabet_size * self.ITERATIONS):
            if modular_inverse(i, multiplication.alphabet_size) != -1:
                message = multiplication.decode(i, encrypted_message, False,
                                                True)
                if self._verify_text(message):
                    return message
        return None

    def _decrypt_affine(self, encrypted_message):
        """
        Try to brute force Affine encryption

        :param encrypted_message: the message to decrypt
        :return: decrypted message | None
        """
        affine = Affine()
        for i in range(affine.alphabet_size * self.ITERATIONS):
            if modular_inverse(i, affine.alphabet_size) != -1:
                for j in range(affine.alphabet_size):
                    message = affine.decode((i, j), encrypted_message, False,
                                            True)
                    if self._verify_text(message):
                        return message
        return None

    def _decrypt_unbreakable(self, encrypted_message):
        """
        Try to brute force Unbreakable encryption

        :param encrypted_message: the message to decrypt
        :return: decrypted message | None
        """
        unbreakable = Unbreakable()
        for word in self.dictionary.keys():
            message = unbreakable.decode(word, encrypted_message, False, True)
            if self._verify_text(message):
                return message
        return None

    def operate_cipher(self, message):
        """
        Try different decryption algorithms until a proper message is generated
        :param message: the message to decrypt
        :return: decrypted message | None
        """
        # Quit if message is RSA encrypted
        if isinstance(message, list):
            print('[FAILURE]: Cannot decrypt RSA')
            return

        # Try Caesar
        print('[STATUS]: Hacking Caesar encryption...')
        self._decrypted_message = self._decrypt_caesar(message)
        if self._is_verified():
            return self._decrypted_message

        # Try Multiplication
        print('[STATUS]: Hacking Multiplication encryption...')
        self._decrypted_message = self._decrypt_multiplication(message)
        if self._is_verified():
            return self._decrypted_message

        # Try Affine
        print('[STATUS]: Hacking Affine encryption...')
        self._decrypted_message = self._decrypt_affine(message)
        if self._is_verified():
            return self._decrypted_message

        # Try Unbreakable
        print('[STATUS]: Hacking Unbreakable encryption...')
        self._decrypted_message = self._decrypt_unbreakable(message)
        if self._is_verified():
            return self._decrypted_message

        # Failure
        print('[FAILURE]: Failed to decrypt message...')
