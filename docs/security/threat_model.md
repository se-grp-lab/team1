# VAMC Security Threat Model & Invariants
**Author:** Soubhagya (`@Soubhagya981999`)

## 1. Threat Vectors Addressed
1. **Unprivileged Memory Scraping / Cold Boot Attacks**:
   - *Mitigation*: Audio bytearrays are allocated in isolated memory and explicitly zeroed with `0x00` in-place.
2. **Plaintext Credential Harvest**:
   - *Mitigation*: Spotify client secrets and refresh tokens are stored exclusively in OS native keyrings (Secret Service / KWallet / Keychain).
3. **Federated Model Poisoning**:
   - *Mitigation*: Pre-aggregation checks reject $L_2$ norm violations and non-finite `NaN`/`Inf` weights.
