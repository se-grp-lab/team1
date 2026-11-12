# Multimedia Player IPC Protocol Specification
**Author:** Aadya Arvind (`@AadyaArvind19`)

## 1. MPV UNIX Domain Socket IPC
- **Socket Path**: `/tmp/mpvsocket`
- **Protocol**: JSON-RPC 2.0 (newline-delimited UTF-8)
- **Sample Request**:
  ```json
  {"command": ["set_property", "pause", true]}
  ```
- **Sample Response**:
  ```json
  {"error": "success", "data": null}
  ```

## 2. VLC Remote Control Socket Interface
- **Transport**: TCP Socket on `127.0.0.1:4212`
- **Delimiter**: `\r\n`
- **Sample Commands**:
  - `pause\r\n`
  - `volume 256\r\n` (Volume range: 0-512)
  - `seek +15\r\n`
