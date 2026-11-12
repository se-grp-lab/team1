# Dynamic Media Player Priority & Fallback Decision Matrix
**Author:** Aadya Arvind (`@AadyaArvind19`)

## Resolution Hierarchy
```
Explicit Player Specified? ("on mpv")
  ├─► YES: Route directly to requested player controller
  └─► NO: Inspect active operating system processes
        ├─► mpv running? -> Target MPV
        ├─► vlc running? -> Target VLC
        ├─► spotify running? -> Target Spotify
        └─► none running? -> Fallback to system mock default controller
```
