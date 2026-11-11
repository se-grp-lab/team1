# Software Test Plan (IEEE 829 Standard)
## Project: Voice Assistant for Multimedia Controls (VAMC)
**Document Identifier:** VAMC-STP-001  
**Version:** 2.0 (Post Sprint 2 Finalization)  
**Date:** November 2026  
**Authors:** Team 1 (Andey Hemanth, Aadya Arvind, Aakash Sharma, Soubhagya)  

---

## 1. Introduction & Objectives
The Voice Assistant for Multimedia Controls (VAMC) is a low-latency, privacy-first, offline-capable voice assistant engineered to command desktop and streaming media players (VLC, MPV, Spotify) without polluting playback audio. 

This test plan defines the testing strategy, tools, scope, and validation criteria for the VAMC system following Sprints 1 and 2. The primary objective is to verify that all functional requirements (FRs) and non-functional requirements (NFRs) specified in the IEEE Software Requirements Specification (SRS) are met with high code and branch coverage, deterministic latency budgets, and rigorous security enforcement.

---

## 2. Traceability Matrix to SRS

| SRS Requirement ID | Description | Test Suite / Module | Verification Method |
|:---|:---|:---|:---|
| **FR-01** | Wake word & Push-to-Talk activation | `tests/test_audio.py` | Unit / Mock Audio Stream |
| **FR-02** | Voice Activity Detection (VAD) | `tests/test_audio.py` | Energy-based Silence Trimming |
| **FR-03** | Offline Speech-to-Text (ASR) | `tests/test_nlu.py`, `tests/test_audio.py` | Local Whisper / Vosk Engine Mock |
| **FR-04** | Intent Parsing & Slot Extraction | `tests/test_intent_parser.py` | Rule-based & Regex Parsing |
| **FR-05** | Local Player IPC (VLC / MPV) | `tests/test_ipc_players.py` | UNIX Domain Socket & RC Protocol |
| **FR-06** | Spotify Web API Integration | `tests/test_spotify_router.py` | Mocked REST API Endpoint Calls |
| **FR-07** | Dynamic Media Player Routing | `tests/test_spotify_router.py` | Active Process & Priority Routing |
| **FR-08** | Visual-Only Feedback (Zero Audio Pollution) | `tests/test_alias_and_feedback.py` | Feedback Emission & Sound Invariant |
| **FR-09** | Translucent Silent HUD Overlay | `tests/test_hud.py` | Non-focus Stealing Overlay State |
| **FR-10** | Display & Playback Rate Controls | `tests/test_display_controls.py` | Subtitle & Fullscreen IPC Payloads |
| **NFR-01** | Latency Budget (< 1000ms End-to-End) | `tests/test_e2e_latency.py` | 100-run Benchmark Timing (< 100ms avg) |
| **NFR-02** | Zero Audio Pollution Guarantee | `tests/test_alias_and_feedback.py` | Audio output stream verification |
| **NFR-03** | Secure Credential Storage | `tests/test_security.py` | Keyring integration & plaintext denial |
| **NFR-04** | Volatile RAM Audio Zeroization | `tests/test_security.py` | Memory buffer overwrite & garbage check |
| **NFR-05** | Differentially Private Edge Adaptation | `tests/test_learning.py` | $\epsilon$-budget tracking & DP-FedAvg |
| **NFR-06** | Mathematical Robustness / Anti-Bypass | `tests/test_learning.py` | NaN/Inf weight rejection tests |

---

## 3. Test Items & Scope
### 3.1 Items Tested
- Ingestion pipeline: Wake-word trigger, hotkey push-to-talk, VAD audio clipping.
- Natural Language Understanding: Intent classification, slot extraction, user alias translation.
- Dispatcher & Player Controllers: MPV JSON IPC, VLC socket IPC, Spotify Web API, fallback routing.
- Visual Subsystem: HUD overlay event lifecycle, non-focus stealing behavior, auto-dismiss timers.
- Security & Privacy: Native OS keyring credentials, explicit RAM zeroization of PCM buffers.
- Acoustic Adaptation & Federated Learning: Local SGD adaptation, L2 gradient clipping, Gaussian noise DP aggregation.

### 3.2 Items Excluded
- Third-party Spotify servers availability (simulated via mock HTTP client).
- Physical microphone hardware variations (tested via byte-stream PCM fixtures).

---

## 4. Test Environment & Execution Strategy
- **Platform:** Linux (Ubuntu/Debian, Fedora, Arch) / POSIX
- **Runtimes:** Python 3.11+, `uv` virtual environment
- **Frameworks:** `pytest 9.x`, `pytest-cov`, `pytest-subtests`
- **Sockets / IPC:** Local UNIX domain sockets (`/tmp/mpvsocket`, `/tmp/vlc.sock`)
- **Execution Command:**
  ```bash
  uv run --with pytest-cov pytest -v --cov=src --cov-branch --cov-report=html:docs/reports/coverage
  ```

---

## 5. Pass/Fail Criteria & Quality Gates
1. **100% Pass Rate:** All 79 automated test units must pass with 0 failures or errors.
2. **Statement Coverage Gate:** Minimum 80% total code coverage (Achieved: **86%**).
3. **Branch Coverage Gate:** Minimum 80% total branch coverage (Achieved: **86%**).
4. **Latency Budget:** End-to-end pipeline execution from audio frame to IPC dispatch must be $< 1000\text{ ms}$ (Achieved: median $< 35\text{ ms}$ simulated).

### 5.1 Security & Privacy Validation Protocol
- **Credential Storage:** `tests/test_security.py` verifies credentials are never persisted to disk in plaintext. If the OS keyring is unavailable, fallback to unencrypted disk is strictly rejected.
- **RAM Zeroization:** Audio chunks in volatile memory are overwritten with zeros (`b'\x00' * len(chunk)`) immediately post-ASR processing.
- **Federated Learning Budget & Anti-Bypass:** Non-finite values (`NaN`, `Inf`) and malformed gradient shapes submitted to the federated aggregation pipeline are rejected with explicit `ValueError` before consumption, ensuring mathematical integrity and preventing privacy budget bypass.

---

## 6. Comprehensive Test Case Specifications

| Test Case ID | Requirement | Test Objective | Input Data | Expected Output | Status |
|:---|:---|:---|:---|:---|:---|
| **TC-AUD-01** | FR-01 | Verify push-to-talk activation | Key press trigger event | Ingestion state switches to `RECORDING` | PASS |
| **TC-AUD-02** | FR-02 | Verify VAD silence clipping | PCM with 1.5s leading silence | Leading silence trimmed; speech preserved | PASS |
| **TC-NLU-01** | FR-04 | Verify intent extraction ("pause") | "pause the music" | Intent: `PAUSE`, Player: `auto` | PASS |
| **TC-NLU-02** | FR-04 | Verify volume adjustment slot | "set volume to 80" | Intent: `SET_VOLUME`, Slot: `80` | PASS |
| **TC-IPC-01** | FR-05 | Verify MPV socket IPC dispatch | Intent `SEEK -10` | JSON IPC: `{"command": ["seek", -10, "relative"]}` | PASS |
| **TC-IPC-02** | FR-05 | Verify VLC socket IPC dispatch | Intent `VOLUME 150` | Scaled to VLC 0-512 range | PASS |
| **TC-SPO-01** | FR-06 | Verify Spotify auth token failure | No token in keyring | Raises `AuthenticationError` | PASS |
| **TC-SPO-02** | FR-06 | Verify Spotify pause REST call | Valid token + device ID | HTTP PUT `/v1/me/player/pause` sent | PASS |
| **TC-ROU-01** | FR-07 | Verify dynamic fallback routing | MPV running, VLC stopped | Dispatches to MPV controller | PASS |
| **TC-ROU-02** | FR-07 | Verify explicit player override | "tell spotify to play" | Routes to Spotify even if MPV active | PASS |
| **TC-HUD-01** | FR-09 | Verify non-focus stealing overlay | Feedback event fired | HUD renders without activating window focus | PASS |
| **TC-HUD-02** | FR-09 | Verify HUD auto-dismiss timer | Event timestamp $t$ | Overlay dismissed after timeout window | PASS |
| **TC-SEC-01** | NFR-03 | Verify keyring credential isolation | "client_secret" payload | Keyring stores securely; no plaintext file | PASS |
| **TC-SEC-02** | NFR-04 | Verify volatile RAM zeroization | Raw PCM audio buffer | Memory overwritten with zero bytes | PASS |
| **TC-FED-01** | NFR-05 | Verify DP epsilon accumulation | 3 consecutive client rounds | Epsilon budget decrements accurately | PASS |
| **TC-FED-02** | NFR-06 | Verify NaN gradient rejection | Vector containing `[0.1, NaN]` | Rejected with `ValueError`; budget untouched | PASS |
| **TC-LAT-01** | NFR-01 | Verify 100-run pipeline latency | 100 simulated commands | 100% execute under 100ms; avg $< 35\text{ms}$ | PASS |
