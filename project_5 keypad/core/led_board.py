"""LED Board Simulator Module"""

import time
from . import GPIOSimulator_v5


class LEDBoard():
    """Charlieplexed LED Board Simulator"""

    def __init__(self):
        self.gpio = GPIOSimulator_v5.GPIOSimulator()
        self.c_pin_0 = GPIOSimulator_v5.PIN_CHARLIEPLEXING_0
        self.c_pin_1 = GPIOSimulator_v5.PIN_CHARLIEPLEXING_1
        self.c_pin_2 = GPIOSimulator_v5.PIN_CHARLIEPLEXING_2
        self.pin_settings = {
            1: [self.c_pin_2, self.c_pin_0, self.c_pin_1,
                self.c_pin_0, self.gpio.HIGH, self.c_pin_1, self.gpio.LOW],
            2: [self.c_pin_2, self.c_pin_0, self.c_pin_1,
                self.c_pin_0, self.gpio.LOW, self.c_pin_1, self.gpio.HIGH],
            3: [self.c_pin_0, self.c_pin_1, self.c_pin_2,
                self.c_pin_1, self.gpio.HIGH, self.c_pin_2, self.gpio.LOW],
            4: [self.c_pin_0, self.c_pin_1, self.c_pin_2,
                self.c_pin_1, self.gpio.LOW, self.c_pin_2, self.gpio.HIGH],
            5: [self.c_pin_1, self.c_pin_0, self.c_pin_2,
                self.c_pin_0, self.gpio.HIGH, self.c_pin_2, self.gpio.LOW],
            6: [self.c_pin_1, self.c_pin_0, self.c_pin_2,
                self.c_pin_0, self.gpio.LOW, self.c_pin_2, self.gpio.HIGH],
        }

    def light_led(self, pin):
        """Turn on one of the 6 LEDs

        Args:
            pin (integer): pin number of LED to turn on (1-6)
        """
        pin_settings = self.pin_settings[pin]
        self.gpio.setup(pin_settings[0], self.gpio.IN)
        self.gpio.setup(pin_settings[1], self.gpio.OUT)
        self.gpio.setup(pin_settings[2], self.gpio.OUT)
        self.gpio.output(pin_settings[3], pin_settings[4])
        self.gpio.output(pin_settings[5], pin_settings[6])
        self.gpio.show_leds_states()

    def flash_all_leds(self, k):
        """Flash all LEDs on and off for k seconds

        Args:
            k (integer): number of seconds to turn on and off lights for
        """
        for _ in range(k):
            self.light_led(1)
            self.light_led(2)
            self.light_led(3)
            self.light_led(4)
            self.light_led(5)
            self.light_led(6)
            time.sleep(1)

    def twinkle_all_leds(self, k):
        """Turn all LEDs on and off in sequence for k seconds

        Args:
            k (integer): Num seconds to turn on and off lights in sequence for
        """
        for _ in range(k):
            self.light_led(3)
            self.light_led(4)
            time.sleep(0.1)
            self.light_led(2)
            self.light_led(5)
            time.sleep(0.1)
            self.light_led(1)
            self.light_led(6)
            time.sleep(0.8)

    def turn_off_all_leds(self):
        """Turns off all leds"""
        self.gpio.cleanup()

    def power_up(self):
        """Light show for power up"""
        for i in range(6):
            self.light_led(i + 1)
            time.sleep(0.1)

    def power_down(self):
        """Light show for power down"""
        for i in range(6, 0, -1):
            self.light_led(i)
            time.sleep(0.1)

    def show_led_states(self):
        """
        Shows the led states
        """
        self.gpio.show_leds_states()


LED = LEDBoard()
LED.light_led(1)
