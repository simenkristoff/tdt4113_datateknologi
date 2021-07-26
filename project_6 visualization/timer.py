"""Timer module"""
import time


class Timer:
    """Timer Class"""
    def __init__(self, name="method"):
        """
        Create a new timer instance, and start the counting
        :param name: method name to print when timer is stopped
        """
        self._start_time = time.time_ns()
        self._name = name

    def print_name(self):
        """Print the current method name"""
        print(self._name)

    def stop(self):
        """
        Stop the timer
        :return: time elapsed since timer started
        """
        difference = time.time_ns() - self._start_time
        print(f"Time elapsed doing {self._name}: {difference / 1e9:.2f}s")
        return difference
