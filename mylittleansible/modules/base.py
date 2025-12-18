"""Base module class for MyLittleAnsible."""

from abc import ABC, abstractmethod
from typing import Any, Dict

from mylittleansible.utils import CmdResult
from paramiko import SSHClient


class BaseModule(ABC):
    """Abstract base class for all MyLittleAnsible modules."""

    name: str = "base"

    def __init__(
        self,
        params: Dict[str, Any],
        dry_run: bool = False,
        changed_threshold: bool = True,
    ) -> None:
        """
        Initialize a module.

        Args:
            params: Dictionary of parameters for the module
            dry_run: If True, simulate without executing
            changed_threshold: If True, mark task as changed
        """
        self.params = params
        self.dry_run = dry_run
        self.changed = changed_threshold

    def check_required_params(self, required: list) -> None:
        """
        Check if all required parameters are present.

        Args:
            required: List of required parameter names

        Raises:
            ValueError: If any required parameter is missing
        """
        missing = [p for p in required if p not in self.params]
        if missing:
            raise ValueError(f"Missing required parameters: {', '.join(missing)}")

    @abstractmethod
    def process(self, ssh_client: SSHClient) -> CmdResult:
        """
        Process the module logic.

        Args:
            ssh_client: Active SSH connection

        Returns:
            CmdResult with execution details
        """
        pass

    def execute(self, ssh_client: SSHClient) -> CmdResult:
        """
        Execute the module with dry-run support.

        Args:
            ssh_client: Active SSH connection

        Returns:
            CmdResult with execution details
        """
        if self.dry_run:
            return CmdResult(
                stdout=f"[DRY-RUN] Would execute {self.name} with params: {self.params}",
                stderr="",
                exit_code=0,
                changed=False,
            )

        result = self.process(ssh_client)
        result.changed = self.changed and result.is_success

        return result
