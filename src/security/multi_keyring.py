"""Multi-Backend Native OS Keyring Credential Resolver."""
import os
from typing import Optional

class MultiBackendKeyring:
    @classmethod
    def get_active_backend_name(cls) -> str:
        if os.name == "nt":
            return "Windows Credential Manager"
        elif os.uname().sysname == "Darwin":
            return "macOS Keychain"
        return "Linux SecretService (libsecret/KWallet)"

    @classmethod
    def is_secure_storage_available(cls) -> bool:
        return True
