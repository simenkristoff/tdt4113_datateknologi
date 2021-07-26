""" Project 3 Encryption module """
from random import randint

from cipher.cipher import Cipher
from cipher.cipher_affine import Affine
from cipher.cipher_caesar import Caesar
from cipher.cipher_multiplication import Multiplication
from cipher.cipher_rsa import RSA
from cipher.cipher_unbreakable import Unbreakable
from person.person_hacker import Hacker
from person.person_receiver import Receiver
from person.person_sender import Sender
from utils.utils import random_message

ciphers = [Caesar, Multiplication, Affine, Unbreakable, RSA]


def __delegate_keys(cipher: Cipher):
    """
    Generate and delegate keys for sender and receiver

    :param cipher: the cipher used
    :return: sender, receiver
    """
    cipher = cipher()
    sender, receiver = Sender(cipher), Receiver(cipher)
    sender_keys, receiver_keys = cipher.generate_keys()

    sender.set_key(sender_keys)
    receiver.set_key(receiver_keys)
    return sender, receiver


def __setup_instance(cipher: Cipher = None, impl_hacker: bool = True,
                     message_length: int = 5):
    """
    Setup a message transaction instance with a cipher

    :param cipher: the cipher to use
    :param impl_hacker: implement a hacker, which is tries to decrypt the
    messag by brute force
    :param message_length: the word length of the message
    :return:
    """
    if cipher is None:
        cipher = ciphers[randint(0, len(ciphers) - 1)]

    sender, receiver = __delegate_keys(cipher)
    enc_msg = sender.operate_cipher(random_message(message_length))
    if impl_hacker:
        hacker = Hacker()
        hacker.operate_cipher(enc_msg)
    receiver.operate_cipher(enc_msg)


def main():
    """ Main method """
    __setup_instance(Affine, True, 5)


if __name__ == '__main__':
    main()
