"""HUD Window Positioning and Multi-Monitor Calculations."""
from typing import Tuple

class HUDPositioner:
    @staticmethod
    def calculate_pill_coordinates(
        screen_width: int,
        screen_height: int,
        pill_width: int = 340,
        pill_height: int = 56,
        margin_bottom: int = 48
    ) -> Tuple[int, int]:
        x = max(0, (screen_width - pill_width) // 2)
        y = max(0, screen_height - pill_height - margin_bottom)
        return (x, y)
