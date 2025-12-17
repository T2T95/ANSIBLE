"""Inventory management for MyLittleAnsible."""

from dataclasses import dataclass
from typing import Dict, Any

import yaml


@dataclass
class Inventory:
    """Inventory of hosts from YAML file."""

    inventory_file: str
    hosts: Dict[str, Any]

    @classmethod
    def load(cls, inventory_file: str) -> "Inventory":
        """Load inventory from YAML file.

        Args:
            inventory_file: Path to the inventory YAML file.

        Returns:
            Inventory instance with loaded hosts.
        """
        with open(inventory_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        hosts = data.get("hosts", {}) if data else {}

        return cls(inventory_file=inventory_file, hosts=hosts)
