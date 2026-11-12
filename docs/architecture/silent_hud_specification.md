# Silent HUD Interaction & Animation Architecture
**Author:** Aakash Sharma (`@aakash11019`)

## 1. Zero Audio Pollution Invariant
Traditional smart assistants generate audible synthesized speech or acoustic chimes. VAMC enforces an architectural invariant:
$$\text{Acoustic Output} \equiv 0.0 \text{ dB}$$

## 2. Visual Animation Lifecycle
```
[Event Triggered] -> [Fade In 150ms] -> [Visible State 2000ms] -> [Fade Out 250ms] -> [Destroy/Hide]
```

## 3. Window Manager State Flags
- `_NET_WM_STATE_STAYS_ON_TOP`
- `_NET_WM_WINDOW_TYPE_NOTIFICATION`
- `X11_OVERRIDE_REDIRECT = True` (Prevents window focus stealing)
