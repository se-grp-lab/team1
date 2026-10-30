"""Encrypted credential storage via OS native keyrings (PRJ-SR-002).

Secrets (e.g. Spotify OAuth tokens) are stored only in the platform keyring
(Secret Service / macOS Keychain / Windows Credential Locker) through the
optional `keyring` package. There is deliberately no plaintext file fallback:
if no secure backend exists, operations fail loudly.
"""

from typing import Any, Optional

SERVICE_NAME = "vamc"


class KeyringUnavailable(RuntimeError):
    """Raised when no secure OS keyring backend is available."""


def _default_backend() -> Any:
    try:
        import keyring
        from keyring.backends import fail
    except ImportError as exc:
        raise KeyringUnavailable("install the 'keyring' package (pip install vamc[secure])") from exc
    if isinstance(keyring.get_keyring(), fail.Keyring):
        raise KeyringUnavailable("no secure OS keyring backend found")
    return keyring


class CredentialStore:
    """Thin wrapper over a keyring-compatible backend (get/set/delete_password)."""

    def __init__(self, backend: Optional[Any] = None, service: str = SERVICE_NAME):
        self._backend = backend if backend is not None else _default_backend()
        self.service = service

    def set(self, key: str, secret: str) -> None:
        if not key or not secret:
            raise ValueError("key and secret must be non-empty")
        self._backend.set_password(self.service, key, secret)

    def get(self, key: str) -> Optional[str]:
        return self._backend.get_password(self.service, key)

    def delete(self, key: str) -> None:
        try:
            self._backend.delete_password(self.service, key)
        except Exception:
            # Deleting a missing credential is a no-op.
            pass
