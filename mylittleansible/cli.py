"""Command-line interface for MyLittleAnsible."""

import sys
import click
from mylittleansible.utils import setup_logger
from mylittleansible.ssh_manager import SSHManager
from mylittleansible.inventory import Inventory
from mylittleansible.playbook import Playbook


logger = None


@click.command()
@click.option(
    "-f",
    "--file",
    "playbook_file",
    required=True,
    type=click.Path(exists=True),
    help="Path to playbook YAML file (todos.yml)",
)
@click.option(
    "-i",
    "--inventory",
    "inventory_file",
    required=True,
    type=click.Path(exists=True),
    help="Path to inventory YAML file (inventory.yml)",
)
@click.option("--debug", is_flag=True, default=False, help="Enable debug mode with stacktraces")
@click.option(
    "--dry-run", is_flag=True, default=False, help="Show what would be executed without running"
)
def main(playbook_file: str, inventory_file: str, debug: bool, dry_run: bool):
    """MyLittleAnsible - Infrastructure as Code Tool

    Execute playbooks on remote hosts using SSH.

    Example:
        mla -f todos.yml -i inventory.yml
    """
    global logger

    # Setup logger
    logger = setup_logger(debug=debug)

    try:
        logger.info("Starting MyLittleAnsible")

        if dry_run:
            logger.info("DRY-RUN MODE: No changes will be made")

        # Load inventory
        logger.debug(f"Loading inventory from {inventory_file}")
        inventory = Inventory(inventory_file)

        # Load playbook
        logger.debug(f"Loading playbook from {playbook_file}")
        playbook = Playbook(playbook_file, inventory, dry_run=dry_run)

        # Initialize SSH manager
        ssh_manager = SSHManager()

        # Execute playbook
        logger.info("Executing playbook...")

        # Cleanup
        ssh_manager.close()

        logger.info("Playbook execution completed")
        sys.exit(0)

    except KeyboardInterrupt:
        logger.warning("Interrupted by user")
        sys.exit(130)

    except Exception as e:
        if debug:
            logger.exception("Fatal error:")
        else:
            logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
