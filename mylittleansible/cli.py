"""Command-line interface for MyLittleAnsible with enhanced features."""

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
@click.option(
    "-n",
    "--dry-run",
    is_flag=True,
    help="Simulate execution without making changes",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase verbosity (-v, -vv, -vvv)",
)
def main(playbook_file: str, inventory_file: str, dry_run: bool, verbose: int) -> None:
    """
    Entry point for the MyLittleAnsible CLI.
    
    Loads the inventory and playbook, then executes tasks on all hosts.
    
    Examples:
        mla -f playbook.yml -i inventory.yml
        mla -f playbook.yml -i inventory.yml --dry-run
        mla -f playbook.yml -i inventory.yml -vv
    """
    logger.info("Starting MyLittleAnsible")

    if dry_run:
        logger.warning("Running in DRY-RUN mode - no changes will be made")

    if verbose:
        logger.info("Verbosity level: %d", verbose)

    try:
        inventory = Inventory.load(inventory_file)
        logger.info("Loaded inventory with %d host(s)", len(inventory.hosts))

        playbook = Playbook.load(playbook_file, dry_run=dry_run)
        logger.info("Loaded playbook with %d task(s)", len(playbook.tasks))

        logger.info("Executing playbook...")

        result = playbook.execute(inventory)

        # Exit with appropriate code
        if not result.is_success:
            logger.error("Playbook execution failed")
            raise click.Exit(code=1)

        logger.info("Playbook execution completed successfully")

    except FileNotFoundError as e:
        logger.error("File not found: %s", str(e))
        raise click.Exit(code=1) from e
    except Exception as e:
        logger.error("Playbook execution failed: %s", str(e))
        raise click.Exit(code=1) from e


if __name__ == "__main__":
    main()
