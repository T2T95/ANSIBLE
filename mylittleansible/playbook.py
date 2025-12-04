"""Playbook execution - Parse and execute task lists."""

import logging
from typing import List, Dict, Any, Optional
import yaml
from mylittleansible.ssh_manager import SSHManager
from mylittleansible.inventory import Inventory
from mylittleansible.modules.apt import AptModule
from mylittleansible.modules.copy import CopyModule
from mylittleansible.modules.template import TemplateModule
from mylittleansible.modules.service import ServiceModule
from mylittleansible.modules.command import CommandModule
from mylittleansible.modules.sysctl import SysctlModule

logger = logging.getLogger("mla")


class Playbook:
    """Parse and execute playbooks."""

    def __init__(self, playbook_file: str, inventory: Inventory, dry_run: bool = False):
        self.playbook_file = playbook_file
        self.inventory = inventory
        self.dry_run = dry_run
        self.tasks = []
        self.load()

    def load(self) -> None:
        try:
            with open(self.playbook_file, "r") as f:
                data = yaml.safe_load(f)

            if not isinstance(data, list):
                raise ValueError("Playbook must be a list of tasks")

            self.tasks = data
            logger.info(f"Loaded playbook with {len(self.tasks)} task(s)")

        except FileNotFoundError:
            logger.error(f"Playbook file not found: {self.playbook_file}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in playbook file: {e}")
            raise

    def get_tasks(self) -> List[Dict[str, Any]]:
        return self.tasks

    def validate(self) -> bool:
        for idx, task in enumerate(self.tasks):
            if not isinstance(task, dict):
                raise ValueError(f"Task {idx + 1} must be a dictionary")
            if "module" not in task:
                raise ValueError(f"Task {idx + 1} missing 'module' field")
            if "params" not in task:
                task["params"] = {}
        logger.info("Playbook validation successful")
        return True

    def execute(
        self, ssh_manager: SSHManager, hosts: Optional[List[str]] = None, debug: bool = False
    ) -> Dict[str, Dict[str, Any]]:
        self.validate()
        if hosts is None:
            hosts = self.inventory.get_hosts_list()

        module_map = {
            "apt": AptModule,
            "copy": CopyModule,
            "template": TemplateModule,
            "service": ServiceModule,
            "command": CommandModule,
            "sysctl": SysctlModule,
        }

        total_tasks = len(self.tasks)
        host_ips = [self.inventory.get_host_address(h) for h in hosts]
        logger.info(f"processing {total_tasks} tasks on hosts: {', '.join(host_ips)}")

        results = {host: {"ok": 0, "changed": 0, "failed": 0, "tasks": []} for host in hosts}

        for task_idx, task in enumerate(self.tasks, 1):
            module_name = task.get("module")
            params = task.get("params", {})

            for host in hosts:
                try:
                    host_addr = self.inventory.get_host_address(host)
                    logger.info(
                        f"[{task_idx}] host={host_addr} op={module_name} "
                        + " ".join(f"{k}={v}" for k, v in params.items())
                    )

                    if self.dry_run:
                        logger.info(
                            f"[{task_idx}] host={host_addr} op={module_name} status=DRY_RUN"
                        )
                        results[host]["ok"] += 1
                        continue

                    if module_name in module_map:
                        ssh_client = ssh_manager.connect(
                            host_addr,
                            port=self.inventory.get_host_port(host),
                            username=self.inventory.get_host_username(host),
                            password=self.inventory.get_host_password(host),
                            ssh_key_file=self.inventory.get_host_key_file(host),
                        )

                        module_instance = module_map[module_name](params)
                        result = module_instance.process(ssh_client)

                        status = "CHANGED" if "CHANGED" in result.stdout else "OK"
                        logger.info(
                            f"[{task_idx}] host={host_addr} op={module_name} status={status}"
                        )
                        results[host][status.lower()] += 1
                    else:
                        logger.info(f"[{task_idx}] host={host_addr} op={module_name} status=OK")
                        results[host]["ok"] += 1

                except Exception as e:
                    error_msg = str(e)[:200]
                    logger.error(
                        f"[{task_idx}] host={host_addr} op={module_name} error={error_msg}"
                    )
                    results[host]["failed"] += 1

        logger.info(f"done processing tasks for hosts: {', '.join(host_ips)}")
        for host in hosts:
            host_addr = self.inventory.get_host_address(host)
            res = results[host]
            logger.info(
                f"host={host_addr} ok={res['ok']} changed={res['changed']} fail={res['failed']}"
            )

        return results
