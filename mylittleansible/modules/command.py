"""Command Module for MyLittleAnsible"""

from mylittleansible.modules.base import BaseModule
from mylittleansible.utils import CmdResult
from paramiko import SSHClient


class CommandModule(BaseModule):
    name = "command"

    def process(self, ssh_client: SSHClient) -> CmdResult:
        self.check_required_params(["cmd"])

        cmd = self.params["cmd"]
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        exit_code = stdout.channel.recv_exit_status()

        return CmdResult(
            stdout=stdout.read().decode("utf-8"),
            stderr=stderr.read().decode("utf-8"),
            exit_code=exit_code,
        )
