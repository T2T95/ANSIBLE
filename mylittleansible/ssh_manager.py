"""SSH connection manager for MyLittleAnsible."""

import logging
import socket
from typing import Optional

import paramiko
from paramiko import SSHClient, AutoAddPolicy

from mylittleansible.utils import get_ssh_key_path

logger = logging.getLogger("ssh")


class SSHConnectionError(Exception):
    """Custom exception for SSH connection related errors."""


class SSHManager:
    """
    Simple wrapper around paramiko.SSHClient to manage SSH connections.
    """

    def __init__(
        self,
        hostname: str,
        port: int = 22,
        username: Optional[str] = None,
        password: Optional[str] = None,
        key_file: Optional[str] = None,
        timeout: int = 10,
    ) -> None:
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.key_file = key_file
        self.timeout = timeout
        self.client: Optional[SSHClient] = None

    def connect(self) -> SSHClient:
        """
        Establish an SSH connection and return the connected SSHClient instance.
        """
        if self.client is not None:
            return self.client

        logger.info(
            "Connecting to %s:%s as %s",
            self.hostname,
            self.port,
            self.username or "<default>",
        )

        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())

        try:
            connect_kwargs = {
                "hostname": self.hostname,
                "port": self.port,
                "timeout": self.timeout,
            }

            if self.username:
                connect_kwargs["username"] = self.username

            if self.password:
                connect_kwargs["password"] = self.password

            if self.key_file:
                connect_kwargs["key_filename"] = self.key_file
            else:
                # Use default SSH key (e.g. ~/.ssh/id_rsa) if available
                default_key = get_ssh_key_path()
                if default_key:
                    connect_kwargs["key_filename"] = default_key

            client.connect(**connect_kwargs)
            self.client = client
            logger.info("Successfully connected to %s:%s", self.hostname, self.port)
            return client

        except (paramiko.SSHException, socket.error) as exc:
            logger.error(
                "SSH connection failed to %s:%s: %s", self.hostname, self.port, exc
            )
            client.close()
            raise SSHConnectionError(str(exc)) from exc

    def exec_command(self, command: str):
        """
        Execute a command on the remote host.
        Returns (stdin, stdout, stderr).
        """
        if self.client is None:
            self.connect()

        assert self.client is not None
        logger.debug("Executing command on %s: %s", self.hostname, command)
        return self.client.exec_command(command)

    def open_sftp(self):
        """
        Open an SFTP session on the existing SSH connection.
        """
        if self.client is None:
            self.connect()

        assert self.client is not None
        logger.debug("Opening SFTP session to %s", self.hostname)
        return self.client.open_sftp()

    def close(self) -> None:
        """Close the SSH connection."""
        if self.client is not None:
            logger.info("Closing SSH connection to %s:%s", self.hostname, self.port)
            self.client.close()
            self.client = None
