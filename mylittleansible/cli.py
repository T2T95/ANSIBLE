"""Command-line interface for MyLittleAnsible."""

import click

from mylittleansible.inventory import Inventory
from mylittleansible.playbook import Playbook
from mylittleansible.utils.logger import get_logger

logger = get_logger("mla")


@click.command()
@click.option(
    "-f",
    "--file",
    "playbook_file",
    required=True,
    help="Path to the playbook YAML file",
)
@click.option(
    "-i",
    "--inventory",
    "inventory_file",
    required=True,
    help="Path to the inventory YAML file",
)
def main(playbook_file: str, inventory_file: str) -> None:
    """
    Entry point for the MyLittleAnsible CLI.
    Loads the inventory and playbook, then executes tasks on all hosts.
    """
    logger.info("Starting MyLittleAnsible")

    inventory = Inventory.load(inventory_file)
    logger.info("Loaded inventory with %d host(s)", len(inventory.hosts))

    playbook = Playbook.load(playbook_file)
    logger.info("Loaded playbook with %d task(s)", len(playbook.tasks))

    logger.info("Executing playbook...")

    playbook.execute(inventory)

    logger.info("Playbook execution completed")


if __name__ == "__main__":
    main()
