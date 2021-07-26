""" Keypad module """
import time

from project_5.core.GPIOSimulator_v5 import GPIOSimulator, keypad_row_pins, \
    keypad_col_pins


class Keypad:
    """ Keypad class. Simulates Raspberry Pi key-inputs. """

    # Private fields
    __key_coord = {(0, 0): '1',
                   (0, 1): '2',
                   (0, 2): '3',
                   (1, 0): '4',
                   (1, 1): '5',
                   (1, 2): '6',
                   (2, 0): '7',
                   (2, 1): '8',
                   (2, 2): '9',
                   (3, 0): '*',
                   (3, 1): '0',
                   (3, 2): '#'}

    def __init__(self, gpio: GPIOSimulator()):
        """
        Initializes keypad pins.
        """
        self.__gpio = gpio
        for row_pin in keypad_row_pins:
            # Set row pins to output mode
            self.__gpio.setup(row_pin, self.__gpio.OUT)
        for col_pin in keypad_col_pins:
            # Set col pins to input mode
            self.__gpio.setup(col_pin, self.__gpio.IN, state=self.__gpio.HIGH)

    def poll_keys(self):
        """
        Loops through each row pin and listen to the state change of each
        column pin. The combination of (row, pin) makes up a keypad
        character. The loop breaks when a key press is detected, and returns
        the pressed key.
        """
        __key = None
        while __key is None:
            for row_pin in keypad_row_pins:
                # Set current row to high
                self.__gpio.output(row_pin, self.__gpio.HIGH)
                # Iterate through the column pins and check whether any of
                # them are HIGH
                for col_pin in keypad_col_pins:
                    if self.__gpio.input(col_pin) == self.__gpio.HIGH:
                        # Do nothing while a key is being pressed
                        while self.__gpio.input(col_pin) == self.__gpio.HIGH:
                            pass

                        __key = self.__get_key(row_pin, col_pin)
                        print(f'\nPressed key: {__key}')

                self.__gpio.output(row_pin, self.__gpio.LOW)
            time.sleep(0.01)
        return __key

    def __get_key(self, row_pin, col_pin):
        """
        Returns the key linked to the combination of the given row and column
        pin.
        """
        return self.__key_coord[(row_pin - 3, col_pin - 7)]
