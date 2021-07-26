"""KPC-agent module"""
import time
from threading import Thread

from project_5.core.GPIOSimulator_v5 import GPIOSimulator
from project_5.core.keypad import Keypad
from . import led_board


class KPCAgent:
    """KPC-AGENT class"""
    PASSWORD_PATH = "config/password.txt"

    def __init__(self):
        self._keypad = Keypad(GPIOSimulator())
        self.led_board = led_board.LEDBoard()
        self._password = KPCAgent._read_password()

        self._cump = ""
        self._password = self._read_password()
        self._new_password = ""
        self._signal_queue = []

        self._selected_led = 0
        self._cum_led_time = []

    @property
    def password(self):
        """
        Get the current password of the agent

        :return: the password
        """
        return self._password

    @staticmethod
    def _read_password():
        """
        Read the password from the password.txt file.

        :return: password string
        :raise: TypeError if file format is invalid, i.e password does not
                contain only digits
        """
        with open(KPCAgent.PASSWORD_PATH, 'r+') as _f:
            password = _f.read().strip()
        if not password.isdigit():
            raise TypeError("Password must only contain digits")
        if len(password) < 4:
            raise TypeError("Password must be at least 4 digits")
        return password

    def _write_password(self):
        """
        Write the new password to the text file.

        :return:
        """
        with open(KPCAgent.PASSWORD_PATH, 'w+') as _f:
            _f.write(self._password)

    def light_one_led(self, led, dur):
        """
        Turn a LED on.

        :param led: LED to light up
        :param dur: duration
        :return:
        """
        self.led_board.light_led(led)
        time.sleep(dur)
        self.led_board.turn_off_all_leds()
        self.led_board.show_led_states()

    def light_selected_led(self, _):
        """
        Light the selected LED for the specified amount of time

        :return: None
        """
        if self._cum_led_time:
            self.dtt(self.light_one_led, self._selected_led,
                     int("".join(self._cum_led_time)))
            self._cum_led_time = []

    @staticmethod
    def dtt(func, *args, **kwargs):
        """ Executes any class or function call in a new thread
        to keep everything responsive

        @param func: Function or class to pass
        @param args: Arguments passed to the function
        @return:
        """
        _t = Thread(target=func, args=args, kwargs=kwargs)
        _t.start()

    def flash_leds(self):
        """
        Flash the LED's on the board

        :return:
        """
        self.led_board.flash_all_leds(2)

    def twinkle_leds(self):
        """
        Twinkle the LED's on the board
        :return:
        """
        self.led_board.twinkle_all_leds(1)

    def exit_action(self):
        """Shut down the agent"""
        self.led_board.power_down()

    def reset_password_accumulator(self, _):
        """
        Reset the accumulated password entry and show the power up animation.

        :param _: ignore
        :return:
        """
        self._cump = ""
        self.led_board.power_up()

    def append_next_password_digit(self, signal):
        """
        Append next password digit to the cumulated password.

        :param signal: signal entered by the user, must be of type digit
        :return:
        """
        self._cump += signal

    def append_next_time_digit(self, signal):
        """
        Append next time digit to the cumulated time.

        :param signal: signal entered by the user, must be of type digit
        :return:
        """
        self._cum_led_time += signal

    def cache_password(self, _):
        """
        When creating a new password, cache the new password to verify it later.

        :param _: ignore
        :return:
        """
        self._new_password = self._cump
        self._cump = ""
        self.twinkle_leds()

    def verify_login(self, _):
        """
        Verify that the user logged in with the correct password.

        :param _: ignore
        :return:
        """
        if self._cump == self._password:
            self._signal_queue.append("y")
            self.twinkle_leds()
        else:
            self._signal_queue.append("n")
            self.flash_leds()

    def validate_passcode_change(self, _):
        """
        Confirm that the user entered the same password twice, if so update the
        password.

        :param _: ignore
        :return:
        """
        if self._cump == self._new_password and len(self._new_password) >= 4:
            self._password = self._new_password
            self._write_password()
            self.twinkle_leds()
        else:
            self.flash_leds()

        self.reset_agent(None)

    def select_led(self, digit):
        """
        Select an LED to light up.

        :param digit: LED nr.
        :return:
        """
        self._selected_led = int(digit) + 1

    def fully_activate_agent(self, _):
        """
        Does something
        """
        return

    def reset_agent(self, _):
        """
        Reset the agent

        :param _: ignore
        :return:
        """
        self._cump = ""
        self._signal_queue = []
        self._cum_led_time = []

    def power_down(self, _):
        """
        Power down the agent

        :return:
        """
        self.reset_agent(None)
        self.led_board.power_down()

    def get_next_signal(self):
        """
        Get the next keypad signal, override it if we have a signal in the
        signal queue.

        :return:
        """
        return self._signal_queue.pop() if self._signal_queue \
            else self._keypad.poll_keys()

    @staticmethod
    def do_action(function, signal):
        """
        Does action
        """
        function(signal)
