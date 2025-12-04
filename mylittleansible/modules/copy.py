"""Copy Module for MyLittleAnsible"""

from mylittleansible.modules.base import BaseModule
from mylittleansible.utils import CmdResult
from paramiko import SSHClient
import os


class CopyModule(BaseModule):
    name = "copy"

    def process(self, ssh_client: SSHClient) -> CmdResult:
        self.check_required_params(["src", "dest"])

        src = self.params["src"]
        dest = self.params["dest"]
        backup = self.params.get("backup", False)

        if not os.path.exists(src):
            return CmdResult(
                stdout="",
                stderr=f"Source file does not exist: {src}",
                exit_code=1,
            )

        sftp = ssh_client.open_sftp()
        try:
            if backup:
                backup_cmd = f"cp {dest} {dest}.bak"
                ssh_client.exec_command(backup_cmd)

            sftp.put(src, dest)
            return CmdResult(stdout=f"Copied {src} to {dest}", stderr="", exit_code=0)

        except Exception as e:
            return CmdResult(stdout="", stderr=str(e), exit_code=1)

        finally:
            sftp.close()
