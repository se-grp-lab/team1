# VAMC Natural Language Grammar & Regex Specification
**Author:** Aakash Sharma (`@aakash11019`)

## 1. Intent Classification Hierarchy
Commands are parsed via deterministic regular expressions evaluating greedy tokens:
1. **Scrubbing/Seeking**: `(fast\s+forward|forward|rewind|go\s+back|skip)\s+(\d+)\s*(seconds|s|secs|minutes|mins|m)`
2. **Volume Adjustments**: `(volume|turn\s+it)\s+(up|down|louder|quieter|higher|lower)(\s+by)?\s*(\d+)?%?`
3. **Playback Rate**: `(speed\s+up|slow\s+down|playback\s+speed|rate)\s*(to)?\s*([0-9.]+)x?`
4. **Display & Subtitles**: `(fullscreen|maximize|exit\s+fullscreen|subtitles|captions)`

## 2. Slot Extraction Parameters
- `offset_seconds`: integer (signed)
- `volume_level`: integer ($0 \le v \le 100$)
- `target_player`: string enum (`mpv`, `vlc`, `spotify`)
- `playback_rate`: float ($0.25 \le r \le 2.0$)
