""" Template for Project 1: Morse code """
import time
from GPIOSimulator_v1 import *
GPIO = GPIOSimulator()

MORSE_CODE = {'.-': 'a', '-...': 'b', '-.-.': 'c', '-..': 'd', '.': 'e', '..-.': 'f', '--.': 'g',
              '....': 'h', '..': 'i', '.---': 'j', '-.-': 'k', '.-..': 'l', '--': 'm', '-.': 'n',
              '---': 'o', '.--.': 'p', '--.-': 'q', '.-.': 'r', '...': 's', '-': 't', '..-': 'u',
              '...-': 'v', '.--': 'w', '-..-': 'x', '-.--': 'y', '--..': 'z', '.----': '1',
              '..---': '2', '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
              '---..': '8', '----.': '9', '-----': '0'}


class MorseDecoder():
    """ Morse code class """
    INITIAL_STATE = GPIO.PUD_UP
    INTERVAL = {}
    LED_PIN = {}
    currState = 0
    lastState = INITIAL_STATE
    currCallTimestamp = 0
    lastCallTimestamp = 0
    ledEnabled = False

    currSymbol = ''
    sentence = []
    morse = []


    def __init__(self):
        """
        Initializes the Morse Coder
        """
        # Constants
        MILLIS = 10 ** (-3) # Used to convert sec to ms
        TIME = 300 * MILLIS # Base Time for Morse interval

        # Setup input/output for the GPIO
        GPIO.setup(PIN_BTN, GPIO.IN, self.INITIAL_STATE)  ## Set BUTTON to INPUT mode
        GPIO.setup(PIN_RED_LED_0, GPIO.OUT, GPIO.LOW)  ## Set Red LED to OUTPUT mode
        GPIO.setup(PIN_BLUE_LED, GPIO.OUT, GPIO.LOW)  ## Set Blue LED to OUTPUT mode
        self.LED_PIN = {"RED": PIN_RED_LED_0, "BLUE": PIN_BLUE_LED} # Register pins for RED and BLUE LED
        self.INTERVAL = {"DOT": 1*TIME, "DASH": 2.5*TIME, "SYMBOL": 5*TIME} # Setup time interval

    def start(self, withLed=False):
        """
        Starts the Morse Coder
        @param withLed - enable led blinking
        """
        self.ledEnabled = withLed
        self.decoding_loop()

    def getState(self):
        """ If NEXT STATE is not the opposite of the LAST STATE
        or the input read twice is not equal,
        we can assume a faulty input """
        nextState = GPIO.LOW if self.lastState == GPIO.HIGH else GPIO.HIGH
        if GPIO.input(PIN_BTN) == GPIO.input(PIN_BTN) == nextState:
            self.currState = nextState


    def blinkLed(self, pin):
        """
        Blinks a LED LIGHTS, either ['RED', 'BLUE'],
        """
        led = self.LED_PIN[pin]
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.01)
        GPIO.output(led, GPIO.LOW)


    def onButtonPressed(self):
        """
        Handles the logic when the state of BUTTON goes
        from LOW to HIGH
        """
        pause = time.time() - self.lastCallTimestamp # Register time between state change
        self.lastState = GPIO.HIGH # Update the last state
        self.currCallTimestamp = time.time() # Timestamp the action
        if pause > self.INTERVAL['DASH']:
            if pause <= self.INTERVAL['SYMBOL']:
                return 3 # End SYMBOL
            else:
                return 4 # End WORD

    def onButtonReleased(self):
        """
        Handles the logic when the state of BUTTON goes
        from HIGH to LOW
        """
        duration = time.time() - self.currCallTimestamp # Register time between state change
        self.lastState = GPIO.LOW # Update the last state
        self.lastCallTimestamp = time.time() # Timestamp the action
        if duration <= self.INTERVAL['DOT']:
            if (self.ledEnabled): self.blinkLed("RED")
            return 1 # SYMBOL is a '.'
        else:
            if (self.ledEnabled): self.blinkLed("BLUE")
            return 2 # SYMBOL is a '-'

    def read_one_signal(self):
        """
        Registers the signal from the BUTTON and
        dispatches a signal type for further processing.
        """
        signal = None
        if self.lastState == GPIO.LOW and self.currState == GPIO.HIGH:
            signal = self.onButtonPressed()
        if self.lastState == GPIO.HIGH and self.currState == GPIO.LOW:
            signal = self.onButtonReleased()
        if signal is not None:
            self.process_signal(signal)

    def decoding_loop(self):
        """
        Will run through the loop until a Keyboard Interrupt (CTRL+C) is thrown
        """
        try:
            while True:
                time.sleep(0.01) # Sleep 100 millis
                self.getState()
                ##self.currState = GPIO.input(PIN_BTN)
                self.read_one_signal()

        except KeyboardInterrupt:
            self.handle_symbol_end()
            self.show_message()

    def process_signal(self, signal):
        """
        Processes signals received from the BUTTON input:
        1 = DOT, 2 = DASH, 3 = SYMBOL END, 4 = WORD END
        """
        if signal == 1:
            self.update_current_symbol('.')
        elif signal == 2:
            self.update_current_symbol('-')
        elif signal == 3:
            self.handle_symbol_end()
        elif signal == 4:
            self.handle_word_end()

    def update_current_symbol(self, signal):
        print(signal, end="", flush=True)
        self.currSymbol += signal

    def handle_symbol_end(self):
        print(" ", end="", flush=True)
        if self.currSymbol in MORSE_CODE:
            letter = MORSE_CODE[self.currSymbol]
            self.sentence.append(letter)
            self.morse.append(self.currSymbol + " ")
        self.currSymbol = ""

    def handle_word_end(self):
        print("\n", end="", flush=True)
        self.handle_symbol_end()
        self.sentence.append(" ")
        self.morse.append(" ")

    def show_message(self):
        """
        Prints the message
        """
        print("\n\nYou sent the following message: " + "\n"
              + "".join(self.sentence).strip() + "\n"
              + "".join(self.morse).strip() + "\n")



def main():
    decoder = MorseDecoder()
    decoder.start()


if __name__ == "__main__":
    main()
