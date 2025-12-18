"""Service Module for MyLittleAnsible"""

from mylittleansible.modules.base import BaseModule
from mylittleansible.utils import CmdResult
from paramiko import SSHClient


class ServiceModule(BaseModule):
    name = "service"

    def process(self, ssh_client: SSHClient) -> CmdResult:
        self.check_required_params(["name", "state"])

        service_name = self.params["name"]
        desired_state = self.params.get("state", "started")

        cmd_map = {
            "started": f"sudo systemctl start {service_name}",
            "stopped": f"sudo systemctl stop {service_name}",
            "restarted": f"sudo systemctl restart {service_name}",
            "enabled": f"sudo systemctl enable {service_name}",
            "disabled": f"sudo systemctl disable {service_name}",
        }

        if desired_state not in cmd_map:
            return CmdResult(
                stdout="", stderr=f"Unsupported state {desired_state}", exit_code=1
            )

        cmd = cmd_map[desired_state]
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        exit_code = stdout.channel.recv_exit_status()

        return CmdResult(
            stdout=stdout.read().decode("utf-8"),
            stderr=stderr.read().decode("utf-8"),
            exit_code=exit_code,
        )
