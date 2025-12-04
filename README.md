# MyLittleAnsible

A lightweight, Python-based automation tool inspired by Ansible for remote server management via SSH.

## 📋 Overview

**MyLittleAnsible** is a simplified infrastructure-as-code solution that allows you to automate system administration tasks across multiple Linux servers. It follows Ansible's core concepts: playbooks, inventory files, and reusable modules.

### Key Features

- ✅ **SSH-based remote execution** using Paramiko
- ✅ **YAML-based playbooks** for easy task definition
- ✅ **Modular architecture** - extensible with custom modules
- ✅ **Multi-host support** - execute tasks across multiple servers
- ✅ **Template rendering** - Jinja2 support for dynamic configuration
- ✅ **Detailed logging** - track execution with comprehensive logs

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- SSH access to target Linux servers
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd MyAnsible
```

2. Install the package:
```bash
pip install -e .
```

3. Verify installation:
```bash
mla --help
```

---

## 📖 Usage

### Basic Workflow

1. **Create an inventory file** (`inventory.yml`)
2. **Write a playbook** (`playbook.yml`)
3. **Execute the playbook**:
```bash
mla -f playbook.yml -i inventory.yml
```

### Inventory Format

```yaml
hosts:
  web01:
    ssh_address: 192.168.1.20
    ssh_port: 22
    ssh_user: ubuntu
    ssh_password: password123
  
  web02:
    ssh_address: 192.168.1.21
    ssh_port: 22
    ssh_user: ubuntu
    ssh_password: password123
```

### Playbook Format

```yaml
- module: apt
  params:
    name: nginx
    state: present

- module: service
  params:
    name: nginx
    state: started

- module: command
  params:
    cmd: "systemctl status nginx"
```

---

## 📦 Available Modules

### 1. **apt** - Package Management
Install, update, or remove packages (Debian/Ubuntu).

```yaml
- module: apt
  params:
    name: htop          # Package name
    state: present      # present | absent
```

### 2. **command** - Execute Shell Commands
Run arbitrary shell commands on remote hosts.

```yaml
- module: command
  params:
    cmd: "uptime"       # Command to execute
```

### 3. **service** - Service Management
Manage system services (start, stop, restart, enable, disable).

```yaml
- module: service
  params:
    name: ssh           # Service name
    state: started      # started | stopped | restarted
```

### 4. **sysctl** - System Configuration
Modify kernel parameters and system settings.

```yaml
- module: sysctl
  params:
    name: "net.ipv4.ip_forward"     # Parameter name
    value: "1"                       # Value
```

### 5. **copy** - File Transfer
Copy files from local machine to remote hosts via SFTP.

```yaml
- module: copy
  params:
    src: "local/path/file.txt"       # Local file
    dest: "/remote/path/file.txt"    # Remote destination
```

### 6. **template** - Template Rendering
Render Jinja2 templates with custom variables and deploy to remote hosts.

```yaml
- module: template
  params:
    src: "templates/config.j2"        # Template file
    dest: "/etc/config/app.conf"      # Remote destination
    app_name: "MyApp"                 # Variables available in template
    environment: "production"
```

---

## 📁 Project Structure

```
MyAnsible/
├── mylittleansible/
│   ├── __init__.py
│   ├── cli.py                 # Command-line interface
│   ├── playbook.py            # Playbook parser & executor
│   ├── inventory.py           # Inventory loader
│   ├── utils.py               # Utilities (CmdResult, etc.)
│   └── modules/
│       ├── __init__.py
│       ├── base.py            # Base module class
│       ├── apt.py             # Package management
│       ├── command.py         # Shell command execution
│       ├── service.py         # Service management
│       ├── sysctl.py          # System configuration
│       ├── copy.py            # File transfer
│       └── template.py        # Template rendering
├── examples/
│   ├── playbooks/
│   │   ├── test_apt.yml
│   │   ├── test_command.yml
│   │   ├── test_service.yml
│   │   ├── test_sysctl.yml
│   │   ├── test_copy.yml
│   │   └── test_template.yml
│   ├── inventory/
│   │   └── inventory.yml
│   ├── files/
│   │   └── test.txt
│   └── templates/
│       └── test.j2
├── pyproject.toml             # Project metadata & dependencies
└── README.md                  # This file
```

---

## 🧪 Testing

Run all test playbooks:

```powershell
mla -f examples/playbooks/test_apt.yml -i examples/inventory/inventory.yml
mla -f examples/playbooks/test_command.yml -i examples/inventory/inventory.yml
mla -f examples/playbooks/test_service.yml -i examples/inventory/inventory.yml
mla -f examples/playbooks/test_sysctl.yml -i examples/inventory/inventory.yml
mla -f examples/playbooks/test_copy.yml -i examples/inventory/inventory.yml
mla -f examples/playbooks/test_template.yml -i examples/inventory/inventory.yml
```

### Expected Output

Successful execution shows:
```
2025-11-17 15:35:12 - mla - INFO - Successfully connected to user@host:22
2025-11-17 15:35:12 - mla - INFO - [1] host=192.168.1.23 op=apt status=OK
2025-11-17 15:35:12 - mla - INFO - host=192.168.1.23 ok=1 changed=0 fail=0
2025-11-17 15:35:12 - mla - INFO - Playbook execution completed
```

---

## 🔧 Creating Custom Modules

Create a new module by extending `BaseModule`:

```python
from mylittleansible.modules.base import BaseModule
from mylittleansible.utils import CmdResult
from paramiko import SSHClient

class MyCustomModule(BaseModule):
    name = "mymodule"

    def process(self, ssh_client: SSHClient) -> CmdResult:
        self.check_required_params(["param1"])
        
        # Your logic here
        param1 = self.params["param1"]
        
        # Execute command via SSH
        stdin, stdout, stderr = ssh_client.exec_command(f"your_command {param1}")
        exit_code = stdout.channel.recv_exit_status()
        
        return CmdResult(
            stdout=stdout.read().decode("utf-8"),
            stderr=stderr.read().decode("utf-8"),
            exit_code=exit_code
        )
```

Register it in `mylittleansible/modules/__init__.py`:

```python
from .mymodule import MyCustomModule

__all__ = ["MyCustomModule", ...]
```

---

## 📝 Playbook Examples

### Example 1: Web Server Setup

```yaml
# deploy_webserver.yml
- module: apt
  params:
    name: nginx
    state: present

- module: copy
  params:
    src: "files/nginx.conf"
    dest: "/etc/nginx/nginx.conf"

- module: service
  params:
    name: nginx
    state: started
```

### Example 2: System Configuration

```yaml
# sysconfig.yml
- module: sysctl
  params:
    name: "net.core.somaxconn"
    value: "1024"

- module: sysctl
  params:
    name: "net.ipv4.tcp_max_syn_backlog"
    value: "2048"

- module: command
  params:
    cmd: "sysctl -p"
```

### Example 3: Template Deployment

```yaml
# deploy_config.yml
- module: template
  params:
    src: "templates/app_config.j2"
    dest: "/etc/app/config.yml"
    app_port: "8080"
    log_level: "DEBUG"
    database_host: "db.example.com"
```

---

## ⚙️ Configuration

### CLI Options

```bash
mla [OPTIONS]

Options:
  -f, --file TEXT          Path to playbook file (YAML) [required]
  -i, --inventory TEXT     Path to inventory file (YAML) [required]
  --help                   Show help message
```

### Logging

All execution logs are printed to stdout with timestamps:
- `INFO` - General information and status updates
- `ERROR` - Execution errors and failures
- `WARNING` - Deprecated warnings

---

## 🔐 Security Considerations

- **SSH Keys**: For production, use SSH keys instead of passwords:
  ```yaml
  hosts:
    prod_server:
      ssh_address: 10.0.0.50
      ssh_port: 22
      ssh_user: deploy
      ssh_key: "/path/to/id_rsa"  # Support planned
  ```

- **Credential Management**: Store sensitive data in environment variables or secret management systems, not in playbooks.

- **Network Security**: Ensure SSH access is restricted to authorized IPs only.

---

## 🐛 Troubleshooting

### Connection Timeout
- Verify host is reachable: `ping <host_ip>`
- Check SSH port: `nc -zv <host_ip> 22`
- Verify credentials in inventory file

### Module Not Found
- Ensure module file exists in `mylittleansible/modules/`
- Check module is registered in `__init__.py`
- Reinstall package: `pip install -e .`

### Permission Denied
- Verify SSH user has required permissions
- Use `sudo` in command module when needed (requires NOPASSWD sudoers config)

---

## 📚 Dependencies

- **paramiko** (3.4.0) - SSH protocol implementation
- **jinja2** (3.1.2) - Template rendering
- **click** (8.1.7) - CLI framework
- **pyyaml** (6.0.1) - YAML parsing

---

## 📄 License

This project is provided as-is for educational and learning purposes.

---

## ✨ Future Enhancements

- [ ] SSH key-based authentication
- [ ] Playbook variables and conditions
- [ ] Error handling and rollback
- [ ] Parallel execution optimization
- [ ] Additional modules (user, group, file permissions, firewall)
- [ ] Dry-run mode
- [ ] Task handlers and notifications

---

## 🤝 Contributing

Contributions are welcome! To add new features or modules:

1. Create a new branch
2. Implement your changes
3. Test thoroughly with the provided test playbooks
4. Submit your changes with documentation

---

## 📞 Support

For issues, questions, or suggestions, please refer to the project documentation or contact the maintainers.

---

**Last Updated**: November 17, 2025
**Version**: 0.1.0
