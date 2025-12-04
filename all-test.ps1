# Lance tous les tests MyLittleAnsible
Write-Host "=== Teste du module APT ===" -ForegroundColor Green
mla -f examples/playbooks/test_apt.yml -i examples/inventory/inventory.yml

Write-Host "`n=== Test du module COMMAND ===" -ForegroundColor Green
mla -f examples/playbooks/test_command.yml -i examples/inventory/inventory.yml

Write-Host "`n=== Test du module SERVICE ===" -ForegroundColor Green
mla -f examples/playbooks/test_service.yml -i examples/inventory/inventory.yml

Write-Host "`n=== Test du module SYSCTL ===" -ForegroundColor Green
mla -f examples/playbooks/test_sysctl.yml -i examples/inventory/inventory.yml

Write-Host "`n=== Test du module COPY ===" -ForegroundColor Green
mla -f examples/playbooks/test_copy.yml -i examples/inventory/inventory.yml

Write-Host "`n=== Test du module TEMPLATE ===" -ForegroundColor Green
mla -f examples/playbooks/test_template.yml -i examples/inventory/inventory.yml

Write-Host "`n=== Tous les tests sont terminés ! ===" -ForegroundColor Cyan
