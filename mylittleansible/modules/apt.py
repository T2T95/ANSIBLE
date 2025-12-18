"""APT Module for MyLittleAnsible"""

from mylittleansible.modules.base import BaseModule
from mylittleansible.utils import CmdResult
from paramiko import SSHClient


class AptModule(BaseModule):
    name = "apt"

    def process(self, ssh_client: SSHClient) -> CmdResult:
        self.check_required_params(["name", "state"])
        package = self.params["name"]
        desired = self.params.get("state", "present")

        check_cmd = f"dpkg-query -W -f='${{Status}}' {package} || echo not-installed"
        result = self._run_cmd(ssh_client, check_cmd)
        already_present = "install ok installed" in result.stdout

        if desired == "present" and already_present:
            status = "OK"
            exit_code = 0
        elif desired == "present" and not already_present:
            install_cmd = f"sudo apt-get update && sudo apt-get install -y {package}"
            result = self._run_cmd(ssh_client, install_cmd)
            status = "CHANGED" if result.is_success else "KO"
            exit_code = result.exit_code
        elif desired == "absent" and already_present:
            remove_cmd = f"sudo apt-get remove -y {package}"
            result = self._run_cmd(ssh_client, remove_cmd)
            status = "CHANGED" if result.is_success else "KO"
            exit_code = result.exit_code
        elif desired == "absent" and not already_present:
            status = "OK"
            exit_code = 0
        else:
            status = "KO"
            exit_code = 1

        return CmdResult(
            stdout=f"apt {package} state={desired} status={status}",
            stderr=result.stderr if "result" in locals() else "",
            exit_code=exit_code,
        )

    def _run_cmd(self, ssh_client: SSHClient, command: str) -> CmdResult:
        stdin, stdout, stderr = ssh_client.exec_command(command)
        exit_code = stdout.channel.recv_exit_status()
        return CmdResult(
            stdout.read().decode("utf-8"), stderr.read().decode("utf-8"), exit_code
        )
