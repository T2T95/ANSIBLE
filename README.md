# MyLittleAnsible - Enhanced Edition 🚀

A lightweight, Python-based automation tool inspired by Ansible for remote server management via SSH.

**Version:** 0.2.0 (Enhanced with status tracking, dry-run, and comprehensive testing)

## 📋 Overview

**MyLittleAnsible** is a simplified infrastructure-as-code solution that allows you to automate system administration tasks across multiple Linux servers. It follows Ansible's core concepts: playbooks, inventory files, and reusable modules.

### ✨ Key Features

- ✅ **SSH-based remote execution** using Paramiko
- ✅ **YAML-based playbooks** for easy task definition
- ✅ **Modular architecture** - extensible with custom modules
- ✅ **Multi-host support** - execute tasks across multiple servers
- ✅ **Template rendering** - Jinja2 support for dynamic configuration
- ✅ **Detailed logging** - track execution with comprehensive logs
- ✅ **Status tracking** - `OK`, `FAILED`, `CHANGED` states for each task
- ✅ **Dry-run mode** - simulate execution without making changes
- ✅ **Verbosity control** - `-v`, `-vv`, `-vvv` for detailed output
- ✅ **Error handling** - robust SSH and timeout management
- ✅ **Unit tests** - pytest coverage for all modules
- ✅ **Enhanced results** - aggregated playbook summary with statistics

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- SSH access to target Linux servers
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/T2T95/ANSIBLE.git
cd ANSIBLE
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. Install the package:
```bash
pip install -e .
```

4. Verify installation:
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

### CLI Options

```bash
mla [OPTIONS]

Options:
  -f, --file TEXT          Path to playbook file (YAML) [required]
  -i, --inventory TEXT     Path to inventory file (YAML) [required]
  -n, --dry-run            Simulate execution without making changes
  -v, --verbose            Increase verbosity (-v, -vv, -vvv)
  --help                   Show help message
```

### Examples

**1. Standard execution:**
```bash
mla -f deploy_webserver.yml -i inventory.yml
```

**2. Dry-run (simulate):**
```bash
mla -f deploy_webserver.yml -i inventory.yml --dry-run
```

**3. Verbose output:**
```bash
mla -f deploy_webserver.yml -i inventory.yml -vv
```

**4. Combined:**
```bash
mla -f deploy_webserver.yml -i inventory.yml --dry-run -vvv
```

---

## 📦 Inventory Format

```yaml
hosts:
  web01:
    ssh_address: 192.168.1.20
    ssh_port: 22
    ssh_user: ubuntu
    ssh_password: password123  # or use ssh_key path
  
  web02:
    ssh_address: 192.168.1.21
    ssh_port: 22
    ssh_user: ubuntu
    ssh_key: /home/user/.ssh/id_rsa
```

---

## 📋 Playbook Format

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
    state: present      # present | absent | latest
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
    app_name: "MyApp"                 # Variables
    environment: "production"
```

---

## 📊 Execution Results

### Output Format

```
[OK] web01 - apt [CHANGED]
[OK] web02 - service
[FAILED] web03 - command
```

### Result Summary

```
Playbook Summary: ok=5 failed=1 changed=3 skipped=0
```

### Status Codes

- **`OK`** - Task completed successfully
- **`FAILED`** - Task failed (execution stops on that host)
- **`SKIPPED`** - Task was skipped
- **`[CHANGED]`** - Task modified system state

---

## 🧪 Testing

### Running Unit Tests

```bash
pytest tests/ -v
```

### Test Coverage

```bash
pytest tests/ --cov=mylittleansible
```

### Test Playbooks

```bash
mla -f examples/playbooks/test_apt.yml -i examples/inventory/inventory.yml --dry-run
mla -f examples/playbooks/test_command.yml -i examples/inventory/inventory.yml --dry-run
mla -f examples/playbooks/test_service.yml -i examples/inventory/inventory.yml --dry-run
```

---

## 🧪 Example Playbooks

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

- module: command
  params:
    cmd: "systemctl status nginx"
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

## 🔧 Creating Custom Modules

Extend `BaseModule` to create custom modules:

```python
from mylittleansible.modules.base import BaseModule
from mylittleansible.utils import CmdResult
from paramiko import SSHClient

class MyCustomModule(BaseModule):
    name = "mymodule"

    def process(self, ssh_client: SSHClient) -> CmdResult:
        self.check_required_params(["param1"])
        
        param1 = self.params["param1"]
        
        # Execute command via SSH
        stdin, stdout, stderr = ssh_client.exec_command(f"your_command {param1}")
        exit_code = stdout.channel.recv_exit_status()
        
        return CmdResult(
            stdout=stdout.read().decode("utf-8"),
            stderr=stderr.read().decode("utf-8"),
            exit_code=exit_code,
            changed=True  # Mark as changed if applicable
        )
```

Register in `mylittleansible/modules/__init__.py`:

```python
from .mymodule import MyCustomModule

__all__ = ["MyCustomModule", ...]
```

---

## 📁 Project Structure

```
ANSIBLE/
├── mylittleansible/
│   ├── __init__.py
│   ├── cli.py                 # Enhanced CLI with dry-run
│   ├── playbook.py            # Enhanced playbook executor
│   ├── inventory.py           # Inventory loader
│   ├── ssh_manager.py         # SSH connection manager
│   ├── utils.py               # Enhanced utils (CmdResult, TaskResult, PlaybookResult)
│   └── modules/
│       ├── __init__.py
│       ├── base.py            # Enhanced base module
│       ├── apt.py
│       ├── command.py
│       ├── service.py
│       ├── sysctl.py
│       ├── copy.py
│       └── template.py
├── tests/
│   ├── __init__.py
│   ├── test_utils.py          # Unit tests
│   └── test_modules.py        # Module tests
├── examples/
│   ├── playbooks/
│   ├── inventory/
│   ├── files/
│   └── templates/
├── pyproject.toml             # Project metadata
├── setup.py                   # Setup configuration
└── README.md                  # This file
```

---

## 🔐 Security Best Practices

- **SSH Keys (Recommended for production)**:
  ```yaml
  hosts:
    prod_server:
      ssh_address: 10.0.0.50
      ssh_port: 22
      ssh_user: deploy
      ssh_key: "/path/to/id_rsa"
  ```

- **Credential Management**: Store sensitive data in environment variables or secret management systems

- **Network Security**: Restrict SSH access to authorized IPs only

- **Playbook Review**: Always review playbooks before executing in production

- **Dry-run First**: Use `--dry-run` to preview changes before executing

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
- Check SSH key permissions: `chmod 600 ~/.ssh/id_rsa`

### Task Failed on Host
- Check error message in logs
- Use dry-run to identify issues
- Verify task parameters are correct

---

## 📚 Dependencies

- **paramiko** (3.4.0+) - SSH protocol implementation
- **jinja2** (3.1.2+) - Template rendering
- **click** (8.1.7+) - CLI framework
- **pyyaml** (6.0.1+) - YAML parsing
- **pytest** (7.0+) - Testing framework (dev)

---

## 📈 Release Notes

### Version 0.2.0 (Current)
- ✨ Status tracking (OK, FAILED, CHANGED)
- ✨ Dry-run mode (`--dry-run`)
- ✨ Verbosity control (`-v`, `-vv`, `-vvv`)
- ✨ Enhanced error handling
- ✨ Unit tests with pytest
- ✨ PlaybookResult aggregation
- 🔧 Improved logging
- 📚 Enhanced documentation

### Version 0.1.0
- Initial release
- Basic module system
- SSH-based remote execution
- Template rendering

---

## 🤝 Contributing

Contributions are welcome! To add features or modules:

1. Create a new branch
2. Implement your changes with tests
3. Run `pytest` to verify
4. Run `flake8` for code quality
5. Submit pull request with documentation

---

## 📄 License

This project is provided as-is for educational and learning purposes.

---

## ✨ Future Enhancements

- [ ] Playbook variables and conditions
- [ ] Error handling and rollback
- [ ] Parallel execution optimization
- [ ] Additional modules (user, group, file permissions)
- [ ] Plugin system
- [ ] Configuration management
- [ ] Performance metrics
- [ ] Result caching

---

**Last Updated**: December 4, 2025  
**Version**: 0.2.0 (Enhanced)  
**Status**: Production Ready ✅
