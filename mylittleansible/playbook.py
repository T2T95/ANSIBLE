""""Playbook parser and executor for MyLittleAnsible."""

import logging
import time
from typing import Any, Dict, List

import yaml

from mylittleansible.inventory import Inventory
from mylittleansible.modules import (
    AptModule,
    CommandModule,
    CopyModule,
    ServiceModule,
    SysctlModule,
    TemplateModule,
)
from mylittleansible.ssh_manager import SSHManager
from mylittleansible.utils import TaskResult, PlaybookResult


logger = logging.getLogger("playbook")

# Module registry
MODULES = {
    "apt": AptModule,
    "command": CommandModule,
    "service": ServiceModule,
    "sysctl": SysctlModule,
    "copy": CopyModule,
    "template": TemplateModule,
}


class PlaybookError(Exception):
    """Exception raised for playbook-related errors."""


class Playbook:
    """Represents a playbook with a list of tasks."""

    def __init__(self, tasks: List[Dict[str, Any]], dry_run: bool = False) -> None:
        """
        Initialize a playbook.

        Args:
            tasks: List of task dictionaries
            dry_run: If True, simulate without executing
        """
        self.tasks = tasks
        self.dry_run = dry_run

    @staticmethod
    def load(file_path: str, dry_run: bool = False) -> "Playbook":
        """
        Load a playbook from a YAML file.

        Args:
            file_path: Path to the YAML playbook file
            dry_run: If True, simulate without executing

        Returns:
            Playbook instance

        Raises:
            FileNotFoundError: If file doesn't exist
            PlaybookError: If YAML is invalid
        """
        try:
            with open(file_path, "r") as f:
                data = yaml.safe_load(f)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Playbook file not found: {file_path}") from e
        except yaml.YAMLError as e:
            raise PlaybookError(f"Invalid YAML in {file_path}: {str(e)}") from e

        if not isinstance(data, list):
            raise PlaybookError("Playbook must be a list of tasks")

        logger.info("Loaded playbook with %d task(s)", len(data))
        return Playbook(data, dry_run=dry_run)

    def execute(self, inventory: Inventory) -> PlaybookResult:
        """
        Execute all tasks on all hosts in inventory.

        Args:
            inventory: Target inventory with hosts

        Returns:
            PlaybookResult with aggregated results

        Raises:
            PlaybookError: If execution fails
        """
        result = PlaybookResult()

        for host_name, host_config in inventory.hosts.items():
            logger.info("=" * 60)
            logger.info("Executing tasks on host: %s", host_name)
            logger.info("=" * 60)

            # IMPORTANT : utiliser les clés définies dans inventory.yml
            ssh_manager = SSHManager(
                hostname=host_config.get("host"),
                port=host_config.get("port", 22),
                username=host_config.get("user"),
                password=host_config.get("password"),
                key_file=host_config.get("ssh_key"),
            )

            try:
                ssh_manager.connect()

                for task_idx, task in enumerate(self.tasks, 1):
                    task_result = self._execute_task(
                        host_name, task, ssh_manager, task_idx
                    )
                    result.add_result(task_result)

                    if task_result.status == "FAILED":
                        logger.error(
                            "Task failed on host %s. Stopping execution on this host.",
                            host_name,
                        )
                        break

            except Exception as e:
                logger.error("Error on host %s: %s", host_name, str(e))
                result.add_result(
                    TaskResult(
                        host=host_name,
                        task_name="connection",
                        status="FAILED",
                        message=str(e),
                    )
                )

            finally:
                ssh_manager.close()

        self._print_summary(result)
        return result

    def _execute_task(
        self,
        host_name: str,
        task: Dict[str, Any],
        ssh_manager: SSHManager,
        task_idx: int,
    ) -> TaskResult:
        """Execute a single task on a host."""
        module_name = task.get("module")
        params = task.get("params", {})

        if not module_name:
            logger.warning("Task %d has no module specified", task_idx)
            return TaskResult(
                host=host_name,
                task_name=f"Task {task_idx}",
                status="SKIPPED",
                message="No module specified",
            )

        if module_name not in MODULES:
            logger.error("Unknown module: %s", module_name)
            return TaskResult(
                host=host_name,
                task_name=f"{module_name} (Task {task_idx})",
                status="FAILED",
                message=f"Unknown module: {module_name}",
            )

        try:
            start_time = time.time()

            module_class = MODULES[module_name]
            module = module_class(params, dry_run=self.dry_run)
            cmd_result = module.execute(ssh_manager.client)

            duration = time.time() - start_time

            status = "OK" if cmd_result.is_success else "FAILED"
            message = cmd_result.stdout or cmd_result.stderr

            task_result = TaskResult(
                host=host_name,
                task_name=f"{module_name} (Task {task_idx})",
                status=status,
                changed=cmd_result.changed,
                message=message,
                duration=duration,
            )

            logger.info(str(task_result))
            return task_result

        except Exception as e:
            logger.error("Exception in task %d on host %s: %s", task_idx, host_name, str(e))
            return TaskResult(
                host=host_name,
                task_name=f"{module_name} (Task {task_idx})",
                status="FAILED",
                message=str(e),
            )

    def _print_summary(self, result: PlaybookResult) -> None:
        """Print a summary of the playbook execution."""
        logger.info("=" * 60)
        logger.info(str(result))
        logger.info("=" * 60)
        logger.info("Playbook execution completed")
