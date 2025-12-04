import os
from pathlib import Path
from typing import Optional


class CmdResult:
    """Result of a remote command execution."""

    def __init__(self, stdout: str, stderr: str, exit_code: int):
        self.stdout = stdout
        self.stderr = stderr
        self.exit_code = exit_code

    def is_success(self) -> bool:
        """Check if command executed successfully."""
        return self.exit_code == 0

    def __repr__(self) -> str:
        return f"CmdResult(exit_code={self.exit_code})"


def get_ssh_key_path(ssh_key_file: Optional[str] = None) -> Optional[str]:
    """Get SSH private key path.

    Args:
        ssh_key_file: Custom SSH key file path

    Returns:
        Path to SSH private key or None
    """
    if ssh_key_file:
        key_path = Path(ssh_key_file)
        if key_path.exists():
            return str(key_path.resolve())
        return None

    # Check default SSH key locations
    default_keys = [
        "~/.ssh/id_rsa",
        "~/.ssh/id_dsa",
        "~/.ssh/id_ecdsa",
        "~/.ssh/id_ed25519",
    ]

    for key in default_keys:
        expanded_path = Path(key).expanduser()
        if expanded_path.exists():
            return str(expanded_path)

    return None


def get_current_user() -> str:
    """Get current system user.

    Returns:
        Current username
    """
    return os.getenv("USERNAME") or os.getenv("USER") or "root"
