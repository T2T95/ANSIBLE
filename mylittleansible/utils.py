"""Enhanced utilities for MyLittleAnsible with status tracking."""

import logging
import os
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class CmdResult:
    """Result of a command execution."""

    stdout: str
    stderr: str
    exit_code: int
    changed: bool = False

    def __str__(self) -> str:
        """String representation of the result."""
        status = "✓ OK" if self.exit_code == 0 else "✗ FAILED"
        changed_str = "[CHANGED]" if self.changed else ""
        return f"{status} {changed_str} (exit_code={self.exit_code})"

    @property
    def is_success(self) -> bool:
        """Check if command was successful."""
        return self.exit_code == 0


@dataclass
class TaskResult:
    """Result of a task execution on a single host."""

    host: str
    task_name: str
    status: str  # OK, FAILED, SKIPPED
    changed: bool = False
    message: str = ""
    duration: float = 0.0

    def __str__(self) -> str:
        """String representation of task result."""
        changed_str = " [CHANGED]" if self.changed else ""
        return f"[{self.status}] {self.host} - {self.task_name}{changed_str}"


@dataclass
class PlaybookResult:
    """Overall result of a playbook execution."""

    ok_count: int = 0
    failed_count: int = 0
    changed_count: int = 0
    skipped_count: int = 0
    task_results: list = field(default_factory=list)

    def add_result(self, result: TaskResult) -> None:
        """Add a task result."""
        self.task_results.append(result)
        if result.status == "OK":
            self.ok_count += 1
        elif result.status == "FAILED":
            self.failed_count += 1
        elif result.status == "SKIPPED":
            self.skipped_count += 1

        if result.changed:
            self.changed_count += 1

    def __str__(self) -> str:
        """Summary of playbook execution."""
        return (
            f"Playbook Summary: ok={self.ok_count} failed={self.failed_count} "
            f"changed={self.changed_count} skipped={self.skipped_count}"
        )

    @property
    def is_success(self) -> bool:
        """Check if all tasks succeeded."""
        return self.failed_count == 0


def get_ssh_key_path() -> Optional[str]:
    """Get the default SSH key path."""
    home = os.path.expanduser("~")
    default_key = os.path.join(home, ".ssh", "id_rsa")

    if os.path.exists(default_key):
        return default_key

    return None


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger with timestamp and level."""
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # déjà configuré

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    # ✅ CORRECTION : Sans datefmt %f (Windows incompatible)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
