"""WCAG 2.1 Accessibility Contrast Ratio Calculator."""
def get_luminance(r: int, g: int, b: int) -> float:
    def norm(c: int) -> float:
        s = c / 255.0
        return s / 12.92 if s <= 0.03928 else ((s + 0.055) / 1.055) ** 2.4
    return 0.2126 * norm(r) + 0.7152 * norm(g) + 0.0722 * norm(b)

def contrast_ratio(rgb1: tuple, rgb2: tuple) -> float:
    l1 = get_luminance(*rgb1)
    l2 = get_luminance(*rgb2)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)
