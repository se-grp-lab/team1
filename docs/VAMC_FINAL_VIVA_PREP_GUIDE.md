# VAMC Final Viva & Demo Defense Master Guide
**Project:** Voice Assistant for Multimedia Controls (VAMC)  
**Team 1:** Andey Hemanth, Aadya Arvind, Aakash Sharma, Soubhagya  
**Evaluation Date:** November 2026  
**Repository:** `se-grp-lab/team1` (Branch: `main`)  
**Status:** 0 Open PRs, 0 Open Issues, 79/79 Passing Tests, 86% Code & Branch Coverage  

---

## 1. Executive Summary & Grading Philosophy
The evaluators (Prof. Pavithra and Course Teaching Assistants) focus **heavily on SDLC process adherence** rather than merely the technical novelty of the codebase:
- **Traceability Chain:** $\text{IEEE SRS} \longrightarrow \text{IEEE SAD} \longrightarrow \text{GitHub Backlog / Story Points} \longrightarrow \text{PRs / Code Reviews} \longrightarrow \text{IEEE Test Plan} \longrightarrow \text{Automated Test Reports}$.
- **Individual Attribution:** Every team member is evaluated on the exact user stories and Pull Requests assigned to them on GitHub.
- **Permitted Deviations:** Any changes from the original SRS/SAD are permitted if formally explained as agile evolution during the demo.

---

## 2. Individual Member Defense Cheat-Sheet

### 👤 Member 1: Andey Hemanth (`@Andy34G7`) — Lead Systems Architect
- **Assigned Subsystems:** Audio Ingestion Pipeline, Offline ASR Engine, Central Daemon, CI/CD Pipeline.
- **Assigned Pull Requests:**
  - `PR #48`: Audio Ingestion, Push-to-Talk Hotkey, Energy VAD & Silence Clipping.
  - `PR #49`: Offline Speech Recognition Engine (Local Vosk / Whisper-base inference).
  - `PR #47`: Central Daemon integration, UNIX signal handling, E2E Latency Benchmarking.
- **Key Technical Decisions to Defend:**
  - *Why Offline ASR over Cloud (Google/OpenAI APIs)?* Eliminates network round-trip latency ($\sim 400\text{ms}$ cloud vs. $<50\text{ms}$ local), guarantees $100\%$ air-gapped privacy, and adheres to zero cloud dependency constraints.
  - *Why VAD silence clipping?* Trimming leading/trailing ambient silence before ASR inference cuts audio tensor sizes by $>40\%$, directly lowering transcription compute and latency.
  - *Repository Stewardship:* Conducted code reviews and merged PRs #48-#59; authored the security patch on PR #59 eliminating NaN-bypass in differential privacy aggregation.
- **Tests Authored / Defended:** `tests/test_audio.py`, `tests/test_e2e_latency.py`.

---

### 👤 Member 2: Aadya Arvind (`@AadyaArvind19`) — Media Player & IPC Specialist
- **Assigned Subsystems:** Core Playback State Machine, Local Player IPC (MPV/VLC), Spotify Web API & Dynamic Player Routing.
- **Assigned Pull Requests:**
  - `PR #53`: Core Playback Controller, Volume Clamping, Mute/Unmute State Machine.
  - `PR #51`: Local Player IPC Controllers (MPV JSON IPC over UNIX domain sockets; VLC Remote Control socket on port 4212).
  - `PR #52`: Spotify Web API Controller, OAuth Token Refresh, Dynamic Player Priority Router.
- **Key Technical Decisions to Defend:**
  - *Why UNIX Domain Sockets for MPV and TCP for VLC?* MPV's native IPC runs over `/tmp/mpvsocket` utilizing bi-directional JSON-RPC payloads, providing atomic state responses. VLC uses a line-buffered remote control socket interface (`rc`) with CRLF delimiters.
  - *How Dynamic Routing Works:* When a command like `"pause"` lacks an explicit target player, `PlayerRouter` scans active processes (`pgrep mpv`, `pgrep vlc`). If multiple are running, priority resolves via most recent playback activity (sticky routing) or defined priority (`mpv > vlc > spotify`).
  - *Volume Bounding:* Bounded between $0$ and $100\%$, converted to player-specific linear scales (e.g., VLC's $0-512$ volume range).
- **Tests Authored / Defended:** `tests/test_ipc_players.py`, `tests/test_spotify_router.py`.

---

### 👤 Member 3: Aakash Sharma (`@aakash11019`) — Natural Language & Visual UI Specialist
- **Assigned Subsystems:** Natural Language Understanding (NLU), Custom Alias Dictionary, Zero Audio Pollution Visual Bus, Display Controls, Silent HUD Overlay.
- **Assigned Pull Requests:**
  - `PR #50`: NLU Intent Classification and Slot Extraction (Regex & rule-based parser).
  - `PR #54`: User-Configurable Alias Dictionary & Zero Audio Pollution Visual Bus.
  - `PR #56`: Display Controls (Fullscreen toggle, Playback Rate $0.25\times-2.0\times$, Subtitle tracks).
  - `PR #57`: Silent Translucent HUD Overlay (Non-focus stealing GUI pill, auto-dismiss timers).
- **Key Technical Decisions to Defend:**
  - *Zero Audio Pollution Guarantee:* Conventional voice assistants (Alexa, Siri) speak back or play chime sounds that interrupt media playback. VAMC enforces a strict architectural invariant: **$0$ audio output bytes produced**. Feedback is rendered strictly visually via a translucent HUD pill.
  - *Non-Focus Stealing Overlay:* Uses window manager attributes (`override_redirect`, `-topmost`) so fullscreen movies or games never lose keyboard/mouse focus when a voice command is confirmed.
  - *Display IPC Payloads:* Maps `"speed up"` / `"slow down"` to MPV `["set_property", "speed", <val>]` clamped between $0.25\times$ and $2.0\times$, and toggles subtitle visibility via MPV `sub-visibility` and VLC `sub-track`.
- **Tests Authored / Defended:** `tests/test_intent_parser.py`, `tests/test_alias_and_feedback.py`, `tests/test_display_controls.py`, `tests/test_hud.py`.

---

### 👤 Member 4: Soubhagya (`@Soubhagya981999`) — Security & Edge Intelligence Specialist
- **Assigned Subsystems:** OS Keyring Secret Storage, Volatile RAM Audio Zeroization, On-Device Acoustic Adaptation, Differentially Private Federated Learning.
- **Assigned Pull Requests:**
  - `PR #55`: Acoustic Adapter foundation for phonetic corrections.
  - `PR #58`: Security Credentials Store (Native OS Secret Service) & Volatile RAM Zeroization.
  - `PR #59`: Edge Acoustic Adaptation ($\ge 3$ support threshold) & $(\epsilon, \delta)$-Differentially Private Federated Averaging (DP-FedAvg) with L2 clipping and Gaussian perturbation.
- **Key Technical Decisions to Defend:**
  - *Volatile Memory Zeroization (NFR-04):* ASR engines store PCM voice samples in memory buffers. To defend against cold-boot attacks and unprivileged heap scraping, buffers are explicitly overwritten with `b'\x00' * len(chunk)` immediately post-tokenization.
  - *OS Native Keyring over Config Files:* Third-party API keys (Spotify Client Secret / Refresh Token) are never stored in plaintext YAML/JSON files. They are stored in the host OS keyring (Linux `libsecret`/KWallet, macOS Keychain).
  - *Differential Privacy in Federated Learning (DP-FedAvg):* When sharing acoustic adaptation weight updates with an aggregation server, local model gradient deltas are clipped by their $L_2$ norm ($S$) and perturbed with Gaussian noise $\mathcal{N}(0, \sigma^2 S^2)$, guaranteeing $(\epsilon, \delta)$ differential privacy.
  - *The Security Review Patch (PR #59):* Andey's review caught that adversarial or corrupted clients could inject `float('nan')` or `float('inf')` to bypass privacy budget decrement loops. We enforced pre-aggregation sanitization rejecting non-finite weights with `ValueError`.
- **Tests Authored / Defended:** `tests/test_security.py`, `tests/test_learning.py`.

---

## 3. High-Frequency Viva Questions & Model Answers

### Q1: "Explain how you mapped requirements from SRS to SAD, Backlog, and Test Cases."
> **Answer:** "In our IEEE SRS, we defined 10 Functional Requirements (FR-01 to FR-10) and 6 Non-Functional Requirements (NFR-01 to NFR-06). In the SAD, these requirements were mapped to 4 modular architectural layers: Ingestion, Processing/NLU, Dispatch/IPC, and Feedback/Security. On GitHub Projects, each requirement became a backlog issue with Fibonacci story point estimations (1, 2, 3, 5, 8) and clear acceptance criteria assigned to team members across Sprint 1 and Sprint 2. Finally, in our IEEE 829 Test Plan, we created a bidirectional Traceability Matrix where every requirement corresponds to automated pytest cases in `tests/`."

### Q2: "What were your permitted deviations between design and implementation?"
> **Answer:** "During agile execution, we documented two justified architectural evolutions:
> 1. *Speech Recognition Strategy:* We initially considered cloud speech APIs with local fallback. During Sprint 1 benchmarking, we found cloud roundtrips exceeded our $<1000\text{ms}$ latency budget ($400-600\text{ms}$ network jitter). We pivoted entirely to an offline, quantized ASR engine (Vosk/Whisper-base), bringing inference latency down to $<50\text{ms}$ while fulfilling our air-gapped privacy requirement.
> 2. *User Feedback Mechanism:* The original SRS contemplated standard desktop notifications (`libnotify`). However, OS notification banners steal window focus and play system chime sounds, violating NFR-02 (Zero Audio Pollution). We evolved this into a custom non-focus-stealing translucent HUD pill overlay."

### Q3: "How does the system achieve sub-100ms response latency?"
> **Answer:** "Our median end-to-end latency is $32.1\text{ms}$ (measured across a 100-run benchmark in `tests/test_e2e_latency.py`). This is achieved through three architectural optimizations:
> 1. Energy-based Voice Activity Detection (VAD) that truncates silence frames before feeding raw buffers to ASR.
> 2. Rule-based regex tokenization in the NLU layer, achieving intent classification in $<2\text{ms}$ without slow LLM API calls.
> 3. Direct UNIX domain socket IPC to media players (`/tmp/mpvsocket`), avoiding heavy OS process invocations."

### Q4: "How does your team demonstrate code quality and test coverage?"
> **Answer:** "We implemented an automated CI test suite with 79 tests (and 25 subtests) using `pytest` and `pytest-cov`. We achieved **86% statement coverage** across 1,094 statements and **86% branch coverage** across 266 decision branches. All reports—Unit Test Report, System Validation Report, Code Coverage Report, and Branch Coverage Report—are compiled in IEEE-compliant markdown and XML formats under `docs/reports/`."

---

## 4. Live Demo Execution Commands
To demonstrate the project cleanly during the viva:

### 1. Verification of Entire Test Suite & Reports:
```bash
cd /home/andey/Documents/Sem5/SE/group_project/team1
uv run --with pytest-cov pytest -v --cov=src --cov-branch --cov-report=term-missing
```
*(Confirms 79/79 passed in ~1.6s, 86% coverage).*

### 2. Interactive Terminal Demo:
```bash
uv run python demo_runner.py
```
*(Simulates end-to-end ingestion, player routing, volume adjustments, and HUD feedback).*

### 3. Live Microphone Voice Listener:
```bash
uv run python live_voice_listener.py
```
*(Accepts push-to-talk voice commands into active MPV/VLC players).*

---

## 5. Pre-Viva Checklist for Tomorrow
- [x] All PRs merged into `main` (0 open PRs, 0 open issues).
- [x] IEEE SRS, SAD, and IEEE 829 Test Plan located in `docs/`.
- [x] Unit, System Validation, Code Coverage, and Branch Coverage reports located in `docs/reports/`.
- [x] Sprint 1 outcome video (`VAMC_Sprint1_Demo.mp4`) committed to repo root.
- [x] Working live demo scripts verified (`demo_runner.py`, `live_voice_listener.py`).
- [x] Every team member prepared to speak to their specific PRs and user stories.
