"""Rule module"""

class Rule:
    """Rule class"""

    def __init__(self, state1, state2, signal, action):
        self._state1 = state1
        self._state2 = state2
        self._signal = signal
        self._action = action

    def match(self, state, signal):
        """
        Matches state with signal
        """
        if not isinstance(self._state1, tuple):
            return state == self._state1 and self._signal(signal)
        return state in self._state1 and self._signal(signal)

    @property
    def exit_state(self):
        """
        Exits the current state
        """
        return self._state2

    @property
    def action(self):
        """
        Returns the action
        """
        return self._action
