"""Silent translucent floating HUD pill (VAMC-F-019, VAMC-F-020).

Toolkit-agnostic HUD model: a renderer callback draws the pill, while this class
owns visibility, opacity, auto-dismiss timing and the focus policy. The pill is
always click-through and never takes keyboard focus, so it cannot interrupt the
user's current application.
"""

import time
from dataclasses import dataclass
from typing import Callable, Optional

from .silent_feedback import VisualFeedbackEvent

Renderer = Callable[[Optional["HUDState"]], None]


@dataclass(frozen=True)
class HUDState:
    icon: str
    message: str
    opacity: float
    always_on_top: bool
    accepts_focus: bool
    click_through: bool
    expires_at: float


class HUDOverlay:
    """Floating pill that shows the latest feedback event and dismisses itself."""

    def __init__(self, renderer: Optional[Renderer] = None, dismiss_after_s: float = 2.0,
                 opacity: float = 0.85, clock: Callable[[], float] = time.monotonic):
        if not 0.0 < opacity < 1.0:
            raise ValueError("HUD must be translucent: opacity must be in (0, 1)")
        if dismiss_after_s <= 0:
            raise ValueError("dismiss_after_s must be positive")
        self._renderer = renderer or (lambda state: None)
        self.dismiss_after_s = dismiss_after_s
        self.opacity = opacity
        self._clock = clock
        self.state: Optional[HUDState] = None

    @property
    def visible(self) -> bool:
        return self.state is not None

    def show(self, event: VisualFeedbackEvent) -> HUDState:
        """Displays (or replaces) the pill and restarts the dismiss timer."""
        self.state = HUDState(
            icon=event.icon,
            message=event.message,
            opacity=self.opacity,
            always_on_top=True,
            accepts_focus=False,
            click_through=True,
            expires_at=self._clock() + self.dismiss_after_s,
        )
        self._renderer(self.state)
        return self.state

    def tick(self) -> bool:
        """Dismisses the pill when its timer has elapsed. Returns True if dismissed."""
        if self.state is not None and self._clock() >= self.state.expires_at:
            self.dismiss()
            return True
        return False

    def dismiss(self) -> None:
        """Hides the pill immediately."""
        self.state = None
        self._renderer(None)
