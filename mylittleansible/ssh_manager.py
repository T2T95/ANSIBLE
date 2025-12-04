"""SSH connection management using Paramiko."""

import logging
from typing import Optional, Tuple
from paramiko.ssh_exception import SSHException, AuthenticationException
from mylittleansible.utils import CmdResult, get_ssh_key_path, get_current_user


logger = logging.getLogger("mla")


class SSHManager:
    """Manage SSH connections to remote hosts."""

    def __init__(self):
        """Initialize SSH manager."""
        self.clients = {}  # Cache for SSH clients

    def connect(
        self,
        host: str,
        port: int = 22,
        username: Optional[str] = None,
        password: Optional[str] = None,
        ssh_key_file: Optional[str] = None,
    ) -> SSHClient:
        """Connect to a remote host via SSH.

        Args:
            host: Remote host IP or hostname
            port: SSH port (default: 22)
            username: Username (default: current user)
            password: Password for authentication
            ssh_key_file: Path to private key file

        Returns:
            Connected SSHClient instance

        Raises:
            AuthenticationException: If authentication fails
            SSHException: If SSH connection fails
        """
        # Use cached connection if available
        cache_key = f"{host}:{port}"
        if cache_key in self.clients:
            try:
                # Test if connection is still alive
                self.clients[cache_key].exec_command("echo")
                return self.clients[cache_key]
            except Exception:
                # Connection is dead, remove from cache
                del self.clients[cache_key]

        client = SSHClient()
        client.set_missing_host_key_policy(AutoAddPolicy())

        # Set default username
        if username is None:
            username = get_current_user()

        try:
            # Try authentication methods in order of preference
            if password:
                # Username/password authentication
                logger.debug(f"Connecting to {host}:{port} with user/pass")
                client.connect(
                    host,
                    port=port,
                    username=username,
                    password=password,
                    allow_agent=False,
                    look_for_keys=False,
                )
            elif ssh_key_file:
                # Private key authentication
                logger.debug(f"Connecting to {host}:{port} with key: {ssh_key_file}")
                client.connect(
                    host,
                    port=port,
                    username=username,
                    key_filename=ssh_key_file,
                    allow_agent=False,
                    look_for_keys=False,
                )
            else:
                # Default SSH config (agent + default keys)
                logger.debug(f"Connecting to {host}:{port} with default SSH config")
                client.connect(
                    host,
                    port=port,
                    username=username,
                    allow_agent=True,
                    look_for_keys=True,
                )

            logger.info(f"Successfully connected to {username}@{host}:{port}")
            self.clients[cache_key] = client
            return client

        except AuthenticationException as e:
            logger.error(f"Authentication failed for {username}@{host}: {e}")
            raise
        except SSHException as e:
            logger.error(f"SSH connection failed to {host}: {e}")
            raise

    def run_command(
        self,
        client: SSHClient,
        command: str,
        shell: str = "/bin/bash",
    ) -> CmdResult:
        """Execute a command on the remote host.

        Args:
            client: Connected SSHClient instance
            command: Command to execute
            shell: Shell to use (default: /bin/bash)

        Returns:
            CmdResult with stdout, stderr, and exit code
        """
        # Wrap command in shell if not already in shell syntax
        full_command = f"{shell} -c {repr(command)}" if not command.startswith(shell) else command

        try:
            stdin, stdout, stderr = client.exec_command(full_command)
            exit_code = stdout.channel.recv_exit_status()

            stdout_text = stdout.read().decode("utf-8", errors="ignore")
            stderr_text = stderr.read().decode("utf-8", errors="ignore")

            return CmdResult(stdout=stdout_text, stderr=stderr_text, exit_code=exit_code)
        except Exception as e:
            logger.error(f"Command execution failed: {e}")
            return CmdResult(stdout="", stderr=str(e), exit_code=1)

    def close(self, host: Optional[str] = None, port: int = 22) -> None:
        """Close SSH connection(s).

        Args:
            host: Specific host to disconnect (if None, close all)
            port: SSH port (default: 22)
        """
        if host is None:
            # Close all connections
            for client in self.clients.values():
                try:
                    client.close()
                except Exception:
                    pass
            self.clients.clear()
        else:
            # Close specific connection
            cache_key = f"{host}:{port}"
            if cache_key in self.clients:
                try:
                    self.clients[cache_key].close()
                except Exception:
                    pass
                del self.clients[cache_key]

    def __del__(self):
        """Cleanup: close all connections when object is destroyed."""
        self.close()
