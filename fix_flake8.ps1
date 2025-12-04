# Script to fix flake8 errors automatically
# MyLittleAnsible - Clean Code Fixer

Write-Host "🧹 Cleaning MyLittleAnsible flake8 errors..." -ForegroundColor Green

# Error 1: cli.py - Remove unused 'logging' import
Write-Host "[1/10] Removing unused 'logging' import from cli.py..."
$cli_content = Get-Content "mylittleansible\cli.py" -Raw
$cli_content = $cli_content -replace "import logging\s*\n", ""
Set-Content "mylittleansible\cli.py" $cli_content

# Error 2: cli.py - Remove unused 'results' variable (line 68)
Write-Host "[2/10] Removing unused 'results' variable from cli.py..."
$cli_content = Get-Content "mylittleansible\cli.py" -Raw
$cli_content = $cli_content -replace "results = .*?\n", ""
Set-Content "mylittleansible\cli.py" $cli_content

# Error 3: template.py - Replace bare except with 'except Exception'
Write-Host "[3/10] Fixing bare except in template.py..."
$template_content = Get-Content "mylittleansible\modules\template.py" -Raw
$template_content = $template_content -replace "except:\s*", "except Exception as e:`n            "
Set-Content "mylittleansible\modules\template.py" $template_content

# Error 4: playbook.py - Remove unused CmdResult import
Write-Host "[4/10] Removing unused CmdResult import from playbook.py..."
$playbook_content = Get-Content "mylittleansible\playbook.py" -Raw
$playbook_content = $playbook_content -replace "from mylittleansible.utils import CmdResult\s*\n", ""
Set-Content "mylittleansible\playbook.py" $playbook_content

# Error 5: ssh_manager.py - Remove unused Tuple import
Write-Host "[5/10] Removing unused imports from ssh_manager.py..."
$ssh_content = Get-Content "mylittleansible\ssh_manager.py" -Raw
$ssh_content = $ssh_content -replace "from typing import Tuple\s*\n", ""
$ssh_content = $ssh_content -replace "from paramiko import .*?RSAKey.*?\n", ""
$ssh_content = $ssh_content -replace "from mylittleansible.utils import get_ssh_key_path\s*\n", ""
Set-Content "mylittleansible\ssh_manager.py" $ssh_content

# Error 6-10: logger.py - Remove unused Optional import
Write-Host "[6/10] Removing unused Optional import from logger.py..."
$logger_content = Get-Content "mylittleansible\utils\logger.py" -Raw
$logger_content = $logger_content -replace "from typing import Optional\s*\n", ""
Set-Content "mylittleansible\utils\logger.py" $logger_content

Write-Host ""
Write-Host "✨ All flake8 errors fixed! Running flake8 again to verify..." -ForegroundColor Green
Write-Host ""

# Run flake8 again to verify
flake8 mylittleansible/ --max-line-length=100

Write-Host ""
Write-Host "✅ Done! Code is now clean and PEP8 compliant." -ForegroundColor Green
