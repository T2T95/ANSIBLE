"""Inventory management - Parse and manage hosts configuration."""

import logging
from typing import Dict, Any, List
import yaml


logger = logging.getLogger("mla")


class Inventory:
    """Parse and manage inventory configuration."""

    def __init__(self, inventory_file: str):
        """Initialize inventory from YAML file.

        Args:
            inventory_file: Path to inventory YAML file

        Example inventory.yml:
            hosts:
                webserver:
                    ssh_address: 192.168.1.22
                    ssh_port: 2222
                    ssh_user: bob
                    ssh_password: secret
                bastion:
                    ssh_address: 192.168.1.24
                    ssh_port: 22
        """
        self.inventory_file = inventory_file
        self.hosts = {}
        self.load()

    def load(self) -> None:
        """Load inventory from YAML file."""
        try:
            with open(self.inventory_file, "r") as f:
                data = yaml.safe_load(f)

            if not data or "hosts" not in data:
                raise ValueError("Inventory file must contain 'hosts' section")

            self.hosts = data["hosts"]
            logger.info(f"Loaded inventory with {len(self.hosts)} host(s)")

        except FileNotFoundError:
            logger.error(f"Inventory file not found: {self.inventory_file}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in inventory file: {e}")
            raise

    def get_host(self, hostname: str) -> Dict[str, Any]:
        """Get host configuration by name.

        Args:
            hostname: Host name defined in inventory

        Returns:
            Host configuration dictionary

        Raises:
            KeyError: If host not found
        """
        if hostname not in self.hosts:
            raise KeyError(f"Host '{hostname}' not found in inventory")

        return self.hosts[hostname]

    def get_all_hosts(self) -> Dict[str, Dict[str, Any]]:
        """Get all hosts.

        Returns:
            Dictionary of all hosts
        """
        return self.hosts

    def get_hosts_list(self) -> List[str]:
        """Get list of all host names.

        Returns:
            List of host names
        """
        return list(self.hosts.keys())

    def get_host_address(self, hostname: str) -> str:
        """Get SSH address for a host.

        Args:
            hostname: Host name

        Returns:
            SSH address (IP or hostname)
        """
        host = self.get_host(hostname)
        if "ssh_address" not in host:
            raise ValueError(f"Host '{hostname}' missing 'ssh_address'")
        return host["ssh_address"]

    def get_host_port(self, hostname: str) -> int:
        """Get SSH port for a host.

        Args:
            hostname: Host name

        Returns:
            SSH port (default: 22)
        """
        host = self.get_host(hostname)
        return host.get("ssh_port", 22)

    def get_host_username(self, hostname: str) -> str:
        """Get SSH username for a host.

        Args:
            hostname: Host name

        Returns:
            SSH username (default: None)
        """
        host = self.get_host(hostname)
        return host.get("ssh_user")

    def get_host_password(self, hostname: str) -> str:
        """Get SSH password for a host.

        Args:
            hostname: Host name

        Returns:
            SSH password (default: None)
        """
        host = self.get_host(hostname)
        return host.get("ssh_password")

    def get_host_key_file(self, hostname: str) -> str:
        """Get SSH key file for a host.

        Args:
            hostname: Host name

        Returns:
            SSH key file path (default: None)
        """
        host = self.get_host(hostname)
        return host.get("ssh_key_file")
