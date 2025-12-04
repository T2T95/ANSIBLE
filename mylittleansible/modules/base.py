"""Base module class for all MyLittleAnsible modules."""

from abc import ABC, abstractmethod
from typing import Dict, Any
from paramiko import SSHClient
from mylittleansible.utils import CmdResult


class BaseModule(ABC):
    """Base class for all modules.

    All modules must inherit from this class and implement the process method.
    """

    name: str = "anonymous"

    def __init__(self, params: Dict[str, Any]):
        """Initialize module with parameters.

        Args:
            params: Module parameters from the playbook
        """
        self.params = params

    @abstractmethod
    def process(self, ssh_client: SSHClient) -> CmdResult:
        """Apply the action using the SSH client.

        Args:
            ssh_client: Paramiko SSH client connected to the remote host

        Returns:
            CmdResult with status information
        """
        pass

    def check_required_params(self, required: list) -> None:
        """Validate that required parameters are present.

        Args:
            required: List of required parameter names

        Raises:
            ValueError: If a required parameter is missing
        """
        for param in required:
            if param not in self.params:
                raise ValueError(f"Module '{self.name}' requires parameter '{param}'")
