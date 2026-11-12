"""System Sleep and Suspend Media Event Listener."""
from typing import Callable, List

class SystemSleepHandler:
    def __init__(self, pause_callback: Callable[[], None]):
        self._cb = pause_callback
        self.is_suspended = False

    def on_prepare_for_sleep(self, sleeping: bool):
        if sleeping:
            self.is_suspended = True
            self._cb()
        else:
            self.is_suspended = False
