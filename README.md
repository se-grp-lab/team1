# Voice Assistant for Multimedia Controls (VAMC)

> **Course**: UE24CS341A - Software Engineering  
> **Institution**: Department of Computer Science and Engineering, PES University  
> **Repository**: [se-grp-lab/team1](https://github.com/se-grp-lab/team1)  
> **Document Reference**: [Software Requirements Specification (SRS) v1.0](../../SRS_Voice_Assistant_Multimedia_Controls.md)

---

## Team Information (Team 1)

| S.No | Student Name | SRN / Roll Number | Project Role | GitHub Handle |
| :---: | :--- | :--- | :--- | :--- |
| 1 | **Soubhagya** | `PES2UG25CS827` | Federated Learning & Security Lead | [@Soubhagya981999](https://github.com/Soubhagya981999) |
| 2 | **Aakash Sharma** | `PES2UG24CS010` | UI/UX & Silent Feedback Designer | [@aakash11019](https://github.com/aakash11019) |
| 3 | **Aadya Arvind** | `PES2UG24CS008` | Media Integration & Controls Lead | [@AadyaArvind19](https://github.com/AadyaArvind19) |
| 4 | **Andey Hemanth** | `PES2UG24CS061` | Lead Architect / NLU Specialist | [@Andy34G7](https://github.com/Andy34G7) |

---

## Project Overview

The **Voice Assistant for Multimedia Controls (VAMC)** is an intelligent, privacy-first desktop background service and overlay assistant engineered to deliver touchless control over multimedia playback across multiple environments:
- **Operating System Media**: Global system master volume, mute, and native OS media session keys (Windows SMTC, Linux MPRIS/DBus, macOS MediaRemote).
- **Local Desktop Media Players**: Desktop players including VLC Media Player and MPV via IPC/Telnet APIs.
- **Online & Streaming Platforms**: Streaming services including Spotify (via Spotify Connect / Web API) and YouTube.
- **Core Architecture Constraints**:
  - **Zero Audio Pollution**: 0 dB audio feedback emission during active playback (speech synthesis, beeps, and chimes are strictly prohibited to avoid interrupting listening).
  - **Edge Speech Recognition**: Entirely offline transcription and natural language intent understanding (ASR + NLU).
  - **Silent Heads-Up Display (HUD)**: A translucent, auto-dismissing visual overlay providing instant feedback without stealing window focus.
  - **Differential Privacy**: Edge model fine-tuning with DP-SGD ($\epsilon \le 2.0$) for secure parameter synchronization without raw voice transmission.

---

## Product Backlog & Traceability Matrix

All 26 backlog items are tracked on GitHub with labels, story points (Fibonacci scale), assignees, and sprint milestones.

### Sprint 1: Core Audio Pipeline & Foundations (Oct 12 - Oct 16, 2026) [COMPLETED]
*Committed Velocity: **49 Points** | Completed Velocity: **49 Points (100%)***  
*Milestone: [Sprint 1 (Oct 12 - Oct 16)](https://github.com/se-grp-lab/team1/milestone/1?closed=1) (Status: Closed)*

| Issue | Req ID | User Story Summary | Epic / Category | Priority | Story Points | Assignee | Status |
| :---: | :---: | :--- | :--- | :---: | :---: | :--- | :---: |
| [#1](https://github.com/se-grp-lab/team1/issues/1) | `VAMC-F-001` | Offline Wake Word Monitoring and Acoustic Detection | Audio Ingestion | High | **5** | [@Andy34G7](https://github.com/Andy34G7) | Closed |
| [#2](https://github.com/se-grp-lab/team1/issues/2) | `VAMC-F-002` | Global Push-To-Talk (PTT) Hotkey Activation | Audio Ingestion | High | **3** | [@Andy34G7](https://github.com/Andy34G7) | Closed |
| [#3](https://github.com/se-grp-lab/team1/issues/3) | `VAMC-F-003` | Voice Activity Detection (VAD) & Trailing Silence Clipping | Audio Ingestion | High | **3** | [@Andy34G7](https://github.com/Andy34G7) | Closed |
| [#4](https://github.com/se-grp-lab/team1/issues/4) | `VAMC-F-004` | Embedded Lightweight Offline Automatic Speech Recognition (ASR) | Speech & NLU | High | **5** | [@Andy34G7](https://github.com/Andy34G7) | Closed |
| [#5](https://github.com/se-grp-lab/team1/issues/5) | `VAMC-F-005` | Natural Language Intent Parsing & Entity Parameter Extraction | Speech & NLU | High | **5** | [@Andy34G7](https://github.com/Andy34G7) | Closed |
| [#6](https://github.com/se-grp-lab/team1/issues/6) | `VAMC-F-006` | Configurable Custom Voice Alias Mapping | Speech & NLU | Medium | **3** | [@aakash11019](https://github.com/aakash11019) | Closed |
| [#7](https://github.com/se-grp-lab/team1/issues/7) | `VAMC-F-007` | Core Playback State Control (Play, Pause, Resume, Stop) | Playback Controls | High | **3** | [@AadyaArvind19](https://github.com/AadyaArvind19) | Closed |
| [#8](https://github.com/se-grp-lab/team1/issues/8) | `VAMC-F-008` | Relative Media Scrubbing & Timestamp Seeking | Playback Controls | High | **5** | [@AadyaArvind19](https://github.com/AadyaArvind19) | Closed |
| [#9](https://github.com/se-grp-lab/team1/issues/9) | `VAMC-F-009` | Track Navigation & Playback Mode Toggling | Playback Controls | High | **3** | [@AadyaArvind19](https://github.com/AadyaArvind19) | Closed |
| [#10](https://github.com/se-grp-lab/team1/issues/10) | `VAMC-F-010` | Relative Incremental Volume Adjustment | Volume Management | High | **2** | [@AadyaArvind19](https://github.com/AadyaArvind19) | Closed |
| [#11](https://github.com/se-grp-lab/team1/issues/11) | `VAMC-F-011` | Absolute Exact Percentage Volume Control | Volume Management | High | **3** | [@AadyaArvind19](https://github.com/AadyaArvind19) | Closed |
| [#12](https://github.com/se-grp-lab/team1/issues/12) | `VAMC-F-012` | Instant Audio Mute and Unmute Toggle | Volume Management | High | **2** | [@AadyaArvind19](https://github.com/AadyaArvind19) | Closed |
| [#13](https://github.com/se-grp-lab/team1/issues/13) | `VAMC-NF-001` | End-to-End Command Execution Latency ($\le 400\text{ ms}$) | Performance | High | **5** | [@Andy34G7](https://github.com/Andy34G7) | Closed |
| [#14](https://github.com/se-grp-lab/team1/issues/14) | `VAMC-NF-005` | Zero Audio Pollution Guarantee (0 dB Feedback) | Quality / Audio | High | **2** | [@aakash11019](https://github.com/aakash11019) | Closed |

---

### Sprint 2: Player Integrations, Silent HUD & Privacy (Oct 19 - Oct 23, 2026) [PLANNED]
*Total Story Points Committed: **44 Points***  
*Milestone: [Sprint 2 (Oct 19 - Oct 23)](https://github.com/se-grp-lab/team1/milestone/2)*

| Issue | Req ID | User Story Summary | Epic / Category | Priority | Story Points | Assignee | Status |
| :---: | :---: | :--- | :--- | :---: | :---: | :--- | :---: |
| [#15](https://github.com/se-grp-lab/team1/issues/15) | `VAMC-F-013` | Local Media Player Integration (VLC & MPV IPC) | Player Integrations | High | **5** | [@AadyaArvind19](https://github.com/AadyaArvind19) | Open |
| [#16](https://github.com/se-grp-lab/team1/issues/16) | `VAMC-F-014` | Cloud Streaming Integration (Spotify Web API & Connect) | Player Integrations | High | **5** | [@AadyaArvind19](https://github.com/AadyaArvind19) | Open |
| [#17](https://github.com/se-grp-lab/team1/issues/17) | `VAMC-F-015` | Active Media Player Auto-Detection & Routing | Player Integrations | Medium | **3** | [@AadyaArvind19](https://github.com/AadyaArvind19) | Open |
| [#18](https://github.com/se-grp-lab/team1/issues/18) | `VAMC-F-016` | Video Display Mode & Fullscreen Controls | Display & Subtitles | Medium | **2** | [@aakash11019](https://github.com/aakash11019) | Open |
| [#19](https://github.com/se-grp-lab/team1/issues/19) | `VAMC-F-017` | Voice-Activated Subtitle Toggle & Track Selection | Display & Subtitles | Medium | **3** | [@aakash11019](https://github.com/aakash11019) | Open |
| [#20](https://github.com/se-grp-lab/team1/issues/20) | `VAMC-F-018` | Variable-Speed Playback Rate Adjustment ($0.5\times - 2.0\times$) | Display & Subtitles | Medium | **2** | [@aakash11019](https://github.com/aakash11019) | Open |
| [#21](https://github.com/se-grp-lab/team1/issues/21) | `VAMC-F-019` | Silent Translucent Floating HUD Overlay Pill | Silent HUD UI | High | **5** | [@aakash11019](https://github.com/aakash11019) | Open |
| [#22](https://github.com/se-grp-lab/team1/issues/22) | `VAMC-F-020` | Automatic HUD Auto-Dismiss & Focus Non-Stealing | Silent HUD UI | High | **3** | [@aakash11019](https://github.com/aakash11019) | Open |
| [#23](https://github.com/se-grp-lab/team1/issues/23) | `VAMC-F-021` | Edge-Based Private Acoustic Adaptation (On-Device) | Federated Learning | Medium | **5** | [@Soubhagya981999](https://github.com/Soubhagya981999) | Open |
| [#24](https://github.com/se-grp-lab/team1/issues/24) | `VAMC-F-022` | Differentially Private Federated Weight Synchronization | Federated Learning | Low | **5** | [@Soubhagya981999](https://github.com/Soubhagya981999) | Open |
| [#25](https://github.com/se-grp-lab/team1/issues/25) | `PRJ-SR-001` | Volatile RAM Audio Zeroization & Memory Disposal | Security & Privacy | High | **3** | [@Soubhagya981999](https://github.com/Soubhagya981999) | Open |
| [#26](https://github.com/se-grp-lab/team1/issues/26) | `PRJ-SR-002` | Encrypted Credential Storage via OS Native Keyrings | Security & Privacy | High | **3** | [@Soubhagya981999](https://github.com/Soubhagya981999) | Open |

---

## Story Point Allocation by Assignee

| Team Member | Project Role | Sprint 1 Completed | Sprint 2 Planned | Total Points |
| :--- | :--- | :---: | :---: | :---: |
| **Andey Hemanth** (`@Andy34G7`) | Architecture / ASR & NLU Specialist | **26** | **0** | **26** |
| **Aadya Arvind** (`@AadyaArvind19`) | Media Integration & Controls Lead | **18** | **13** | **31** |
| **Aakash Sharma** (`@aakash11019`) | UI/UX & Silent Feedback Designer | **5** | **15** | **20** |
| **Soubhagya** (`@Soubhagya981999`) | Federated Learning & Security Lead | **0** | **16** | **16** |
| **Total Velocity** | - | **49** | **44** | **93 Points** |

---

## Sprint 1 Verification and Test Results

Sprint 1 implementation includes 16 automated unit and integration tests passing with 100% success rate:
- **Audio Ingestion Test Suite**: Validates wake word detection (<150 ms), global PTT hook triggering (<50 ms), and VAD trailing silence clipping at 500 ms.
- **ASR & Intent Recognition Suite**: Validates offline on-device speech transcription and intent parsing with entity parameter extraction.
- **Alias Resolution Suite**: Validates local alias configuration loading, custom phrase resolution, and disk persistence.
- **Playback & Volume Controller Suite**: Validates play/pause/resume/stop state changes, relative seek delta accuracy, track navigation, step volume, and mute/unmute restoration.
- **Silent Feedback Suite**: Confirms 0 dB audio emission guarantee on all feedback dispatches.
- **End-to-End Latency Benchmark**: 100 runs benchmarking end-to-end command latency, passing well within the <= 400 ms budget (P95 < 0.1 ms on mock reference).

To run the full test suite:
```bash
python3 -m unittest discover -s tests
```

---

## CI/CD Pipeline

The repository includes an automated GitHub Actions CI/CD pipeline configured in `.github/workflows/ci-cd.yml`:
1. **Code Quality & Linting (`lint`)**: Enforces PEP8 syntax and code quality checks using `flake8`.
2. **Multi-Python Test Matrix (`test`)**: Executes all 16 automated unit and integration tests via `pytest` across Python 3.10, 3.11, and 3.12 (as specified in SRS Section 2.4).
3. **NFR Latency & Purity Verification**: Automates latency benchmark verification across 100 runs, verifying the `<= 400 ms` budget (`VAMC-NF-001`) and `0 dB` audio emissions (`VAMC-NF-005`).
4. **Build & Package Artifacts (`build`)**: Packages standard Python distribution wheels (`.whl`) and source tarballs (`.tar.gz`) with automated artifact archiving and job summaries.

