"""Final state machine module"""

from project_5.core.kpc_agent import KPCAgent
from project_5.core.rule import Rule
from project_5.core.state import State


class FSM:
    """FSM class"""

    def __init__(self):
        self._state = State.INIT
        self._rules = []

        self._agent = KPCAgent()
        self._create_rules()

    def _create_rules(self):
        """
        Create a set of rules that we will apply to the FSM

        :return:
        """
        # Initialize fsm and reset password
        self._add_rule(
            Rule(State.INIT, State.READ, lambda s: True,
                 self._agent.reset_password_accumulator))

        # LOGOUT
        self._add_rule(
            Rule((
                State.ACTIVE, State.INIT, State.READ, State.READ2, State.READ3,
                State.LED, State.TIME), State.INIT,
                lambda s: s == '#',
                self._agent.power_down))
        # Add digit to agent temp password
        self._add_rule(Rule(State.READ, State.READ, lambda s: s.isdigit(),
                            self._agent.append_next_password_digit))

        # Go to verify password
        self._add_rule(Rule(State.READ, State.VERIFY, lambda s: s == '*',
                            self._agent.verify_login))

        # Reset agent
        self._add_rule(Rule(State.READ, State.INIT, lambda s: True,
                            self._agent.reset_agent))

        # Password not verified
        self._add_rule(Rule(State.VERIFY, State.INIT, lambda s: s != 'y',
                            self._agent.reset_agent))

        # Fully activate agent
        self._add_rule(Rule(State.VERIFY, State.ACTIVE, lambda s: s == 'y',
                            self._agent.fully_activate_agent))

        # Enter reset password mode
        self._add_rule(Rule(State.ACTIVE, State.READ2, lambda s: s == '*',
                            self._agent.reset_password_accumulator))

        # Verify that we got a digit
        self._add_rule(Rule(State.READ2, State.READ2, lambda s: s.isdigit(),
                            self._agent.append_next_password_digit))

        # Proceed to verify the new password
        self._add_rule(Rule(State.READ2, State.READ3, lambda s: s == '*',
                            self._agent.cache_password))

        # If we did not receive a digit, reset to ACTIVE state
        self._add_rule(Rule(State.READ2, State.ACTIVE, lambda s: True,
                            self._agent.reset_agent))

        # Verify that we got a digit
        self._add_rule(Rule(State.READ3, State.READ3, lambda s: s.isdigit(),
                            self._agent.append_next_password_digit))

        # Proceed to verify the new password
        self._add_rule(Rule(State.READ3, State.ACTIVE, lambda s: s == '*',
                            self._agent.validate_passcode_change))

        # If we did not receive a digit, reset to ACTIVE state
        self._add_rule(Rule(State.READ3, State.ACTIVE, lambda s: True,
                            self._agent.reset_agent))

        # Enter LED mode
        self._add_rule(Rule(State.ACTIVE, State.LED, lambda s: s in "012345",
                            self._agent.select_led))

        # Exit LED mode
        self._add_rule(
            Rule(State.LED, State.ACTIVE, lambda s: s != '*', lambda _: 0))

        # Enter time mode
        self._add_rule(Rule(State.LED, State.TIME, lambda s: s == '*',
                            self._agent.reset_agent))

        # Increment time to display led
        self._add_rule(Rule(State.TIME, State.TIME, lambda s: s.isdigit(),
                            self._agent.append_next_time_digit))

        # Turn the LED on
        self._add_rule(Rule(State.TIME, State.ACTIVE, lambda s: s == '*',
                            self._agent.light_selected_led))

    def _add_rule(self, rule):
        """
        Add a rule to the rules list

        :param rule: the rule to add
        :return: None
        """
        self._rules.append(rule)

    def run(self):
        """
        FSM main loop

        :return:
        """
        while self._state != State.EXIT:
            print(f"\nState: {self._state}, Password:{self._agent.password}")
            signal = self._agent.get_next_signal()
            for rule in self._rules:
                if rule.match(self._state, signal):
                    self._state = rule.exit_state
                    self._agent.do_action(rule.action, signal)
                    break

        self._agent.exit_action()
