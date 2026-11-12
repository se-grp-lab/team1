"""HUD Design Tokens and Geometry Theming (VAMC-UI-001)."""
from dataclasses import dataclass

@dataclass(frozen=True)
class HUDTheme:
    background_rgba: str = "#1e1e2ecc"
    text_color: str = "#cdd6f4"
    accent_color: str = "#89b4fa"
    border_radius_px: int = 24
    padding_vertical_px: int = 12
    padding_horizontal_px: int = 24
    font_family: str = "Inter, -apple-system, system-ui, sans-serif"
    font_size_pt: int = 13
    shadow_blur_px: int = 16
    animation_duration_ms: int = 250
    auto_dismiss_delay_ms: int = 2500

DEFAULT_THEME = HUDTheme()
HIGH_CONTRAST_THEME = HUDTheme(
    background_rgba="#000000fa",
    text_color="#ffffff",
    accent_color="#ffff00",
    border_radius_px=16,
    font_size_pt=15
)
