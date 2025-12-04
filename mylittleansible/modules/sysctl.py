"""Sysctl Module for MyLittleAnsible"""

from mylittleansible.modules.base import BaseModule
from mylittleansible.utils import CmdResult
from paramiko import SSHClient


class SysctlModule(BaseModule):
    name = "sysctl"

    def process(self, ssh_client: SSHClient) -> CmdResult:
        self.check_required_params(["name", "value"])

        name = self.params["name"]
        value = self.params["value"]

        # Apply sysctl setting via command
        cmd = f"sudo sysctl -w {name}={value}"
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        exit_code = stdout.channel.recv_exit_status()

        return CmdResult(
            stdout=stdout.read().decode("utf-8"),
            stderr=stderr.read().decode("utf-8"),
            exit_code=exit_code,
        )
