# 🚀 MyLittleAnsible

> Un outil **Infrastructure as Code** léger pour automatiser la configuration de serveurs Linux distants via SSH

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)]()
[![Licence](https://img.shields.io/badge/Licence-Éducatif-green)]()
[![Status](https://img.shields.io/badge/Status-Production%20Prêt-brightgreen)]()

---

## 📖 Vue d'ensemble

**MyLittleAnsible** est un outil d'automatisation simplifié, basé sur Python, inspiré par **Ansible**, qui vous permet d'automatiser les tâches d'administration système sur plusieurs serveurs Linux en utilisant des **playbooks YAML déclaratifs**.

### Pourquoi MyLittleAnsible?

| Fonctionnalité | MyLittleAnsible | Ansible |
|---|---|---|
| **Courbe d'apprentissage** | ⭐⭐⭐ Facile | ⭐⭐⭐⭐⭐ Complexe |
| **Modules** | 6 modules core | 100+ modules |
| **Temps de setup** | 5 minutes | 30+ minutes |
| **Cas d'usage** | Éducatif + Tâches simples | Automatisation Enterprise |

---

## ✨ Fonctionnalités principales

- ✅ **Exécution SSH distante** - Intégration Paramiko pour connexions sécurisées
- ✅ **Playbooks YAML** - Définitions de tâches simples et lisibles
- ✅ **6 modules core** - apt, copy, template, service, sysctl, command
- ✅ **Support multi-hôtes** - Exécution sur plusieurs serveurs
- ✅ **Mode dry-run** - Aperçu des changements avant exécution (🔥 **BONUS**)
- ✅ **Mode debug** - Stack traces complètes en cas d'erreur (🔥 **BONUS**)
- ✅ **Verbosité** - Niveaux `-v`, `-vv`, `-vvv` (🔥 **BONUS**)
- ✅ **3 méthodes d'authentification SSH** - Mot de passe, clé SSH, défaut (~/.ssh/)
- ✅ **Rendu de templates** - Templates Jinja2 avec variables dynamiques
- ✅ **Idempotence** - Exécution multiple sécurisée (🔥 **BONUS**)
- ✅ **Logging professionnel** - Pas de `print()`, trace complète
- ✅ **Conforme PEP8** - Code propre et maintenable

---

## 🎯 Démarrage rapide

### Prérequis

```bash
Python 3.8+
Accès SSH à des serveurs Linux
pip (gestionnaire de paquets Python)
```

### Installation (5 minutes)

```bash
# 1. Cloner le repository
git clone https://github.com/T2T95/ANSIBLE.git
cd ANSIBLE

# 2. Créer et activer l'environnement virtuel
python -m venv .venv
source .venv/bin/activate                  # Linux/Mac
.\.venv\Scripts\Activate.ps1               # Windows PowerShell

# 3. Installer le package
pip install -e .

# 4. Vérifier l'installation
mla --help
```

---

## 🎬 Utilisation

### Flux de travail standard

```bash
# 1. Créer un fichier inventory (serveurs cibles)
# 2. Écrire un playbook (tâches à exécuter)
# 3. Exécuter le playbook

mla -f playbook.yml -i inventory.yml
```

### Options CLI

```bash
mla [OPTIONS]

Options:
  -f, --file TEXT       Chemin du fichier playbook YAML [obligatoire]
  -i, --inventory TEXT  Chemin du fichier inventory YAML [obligatoire]
  -n, --dry-run         Simuler l'exécution sans effectuer de changements
  -v, --verbose         Augmenter la verbosité (-v, -vv, -vvv)
  --debug               Mode debug (afficher les stack traces complètes)
  --help                Afficher cette aide et quitter
```

### Exemples

```bash
# Exécution standard
mla -f playbook.yml -i inventory.yml

# Simuler sans effectuer de changements (recommandé!)
mla -f playbook.yml -i inventory.yml --dry-run

# Sortie verbose pour déboguer
mla -f playbook.yml -i inventory.yml -vv

# Mode debug (stack traces complet)
mla -f playbook.yml -i inventory.yml --debug

# Combiner les options
mla -f playbook.yml -i inventory.yml --dry-run -vvv
```

---

## 📁 Format de l'inventory

Définissez vos serveurs cibles dans `inventory.yml`:

```yaml
---
hosts:
  webserver1:
    ssh_address: 192.168.1.20
    ssh_port: 22
    ssh_user: ubuntu
    ssh_password: "motdepasse123"
    
  webserver2:
    ssh_address: 192.168.1.21
    ssh_port: 22
    ssh_user: ubuntu
    ssh_key_file: ~/.ssh/id_rsa
```

### Méthodes d'authentification SSH

| Méthode | Configuration | Cas d'usage |
|---|---|---|
| **Défaut** | Aucune config nécessaire | Utilise les clés de ~/.ssh/ |
| **Mot de passe** | `ssh_user` + `ssh_password` | Développement/Tests |
| **Clé SSH** | `ssh_user` + `ssh_key_file` | Production ✅ |

---

## 📋 Format du playbook

Définissez les tâches dans `playbook.yml`:

```yaml
---
- module: apt
  params:
    name: nginx
    state: present

- module: copy
  params:
    src: ./config/nginx.conf
    dest: /etc/nginx/nginx.conf

- module: service
  params:
    name: nginx
    state: started

- module: command
  params:
    command: systemctl status nginx
```

---

## 📦 Modules disponibles

### 1. **apt** - Gestion des paquets

Installer/supprimer/mettre à jour les paquets APT sur Debian/Ubuntu:

```yaml
- module: apt
  params:
    name: nginx              # Nom du paquet
    state: present           # present | absent
```

### 2. **copy** - Transfert de fichiers

Copier les fichiers du local vers les serveurs distants via SFTP:

```yaml
- module: copy
  params:
    src: ./config/app.conf           # Chemin du fichier local
    dest: /etc/app/app.conf          # Destination distante
    backup: true                     # Sauvegarde du fichier existant
```

### 3. **template** - Rendu de templates

Rendre des templates Jinja2 avec des variables:

```yaml
- module: template
  params:
    src: templates/config.j2         # Fichier template
    dest: /etc/app/config.yml        # Destination distante
    app_port: 8080                   # Variables de template
    env: production
```

**Exemple de template** (`config.j2`):

```jinja2
server:
  port: {{ app_port }}
  environment: {{ env }}
  debug: false
```

### 4. **service** - Gestion des services

Gérer les services systemd (démarrer, arrêter, redémarrer, activer, désactiver):

```yaml
- module: service
  params:
    name: nginx              # Nom du service
    state: started           # started | stopped | restarted | enabled | disabled
```

### 5. **sysctl** - Configuration système

Modifier les paramètres du kernel:

```yaml
- module: sysctl
  params:
    attribute: net.core.somaxconn
    value: 8192
    permanent: true          # Rendre permanent (/etc/sysctl.conf)
```

### 6. **command** - Exécuter des commandes shell

Exécuter des commandes shell arbitraires:

```yaml
- module: command
  params:
    command: systemctl status nginx
```

---

## 📊 Résultats d'exécution

### Exemple de sortie

```
2026-01-13 17:40:00,123 - mla - INFO - Démarrage de MyLittleAnsible
2026-01-13 17:40:00,124 - mla - INFO - Inventory chargé avec 2 hôte(s)
2026-01-13 17:40:00,125 - mla - INFO - Playbook chargé avec 3 tâche(s)
2026-01-13 17:40:00,126 - mla - INFO - ============================================================
2026-01-13 17:40:00,127 - mla - INFO - Exécution des tâches sur l'hôte: webserver1
2026-01-13 17:40:00,128 - mla - INFO - [apt (Tâche 1)] OK [CHANGED]
2026-01-13 17:40:00,200 - mla - INFO - [copy (Tâche 2)] OK
2026-01-13 17:40:00,300 - mla - INFO - [service (Tâche 3)] OK [CHANGED]
2026-01-13 17:40:00,350 - mla - INFO - ============================================================
2026-01-13 17:40:00,351 - mla - INFO - Résumé du playbook: ok=3 failed=0 changed=2 skipped=0
```

### Codes de statut

| Statut | Signification |
|---|---|
| **OK** | Tâche exécutée avec succès |
| **OK [CHANGED]** | Tâche a effectué des modifications |
| **FAILED** | Tâche échouée (arrêt sur cet hôte) |
| **SKIPPED** | Tâche ignorée |

---

## 🔧 Architecture

```
┌─────────────────────────────────────────────┐
│  CLI (Click)                                │
│  mla -f playbook.yml -i inventory.yml       │
└────────────────┬────────────────────────────┘
                 │
       ┌─────────┴──────────┐
       ▼                    ▼
   Inventory          Playbook
   (Hôtes YAML)       (Tâches YAML)
       │                    │
       └────────┬───────────┘
                ▼
         Exécuteur de playbook
                │
       ┌────────┴────────┐
       ▼                 ▼
    SSH Manager     Modules (6 types)
  (Paramiko)       (Héritage BaseModule)
```

### Structure du code

```
mylittleansible/
├── cli.py              # Point d'entrée (Click)
├── inventory.py        # Parseur d'inventory
├── playbook.py         # Exécuteur de playbook
├── ssh_manager.py      # Gestion des connexions SSH
├── utils.py            # Structures de données
└── modules/
    ├── base.py         # Classe de module de base
    ├── apt.py          # Module APT
    ├── copy.py         # Module Copy
    ├── template.py     # Module Template
    ├── service.py      # Module Service
    ├── sysctl.py       # Module Sysctl
    └── command.py      # Module Command
```

---

## 💡 Playbooks d'exemple

### Exemple 1: Déployer un serveur web

```yaml
# deploy_web.yml
- module: apt
  params:
    name: nginx-common
    state: present

- module: copy
  params:
    src: ./nginx.conf
    dest: /etc/nginx/nginx.conf

- module: service
  params:
    name: nginx
    state: restarted
    enabled: true

- module: command
  params:
    command: systemctl status nginx
```

**L'exécuter:**

```bash
mla -f deploy_web.yml -i inventory.yml --dry-run  # Aperçu d'abord!
mla -f deploy_web.yml -i inventory.yml             # Exécuter
```

### Exemple 2: Configuration système

```yaml
# sysconfig.yml
- module: sysctl
  params:
    attribute: net.core.somaxconn
    value: 8192
    permanent: true

- module: sysctl
  params:
    attribute: net.ipv4.tcp_max_syn_backlog
    value: 2048
    permanent: true

- module: command
  params:
    command: sysctl -p
```

### Exemple 3: Déploiement de configuration

```yaml
# deploy_config.yml
- module: template
  params:
    src: templates/app_config.j2
    dest: /etc/app/config.yml
    app_name: MonApp
    port: 8080
    environment: production
```

---

## 🧪 Tests

### Tester votre configuration (Dry-Run)

```bash
# Aperçu des changements sans les exécuter
mla -f playbook.yml -i inventory.yml --dry-run

# Avec sortie verbose
mla -f playbook.yml -i inventory.yml --dry-run -vvv
```

### Exécuter les tests unitaires

```bash
# Installer les dépendances de développement
pip install pytest pytest-cov

# Exécuter les tests
pytest tests/ -v

# Vérifier la couverture
pytest tests/ --cov=mylittleansible
```

---

## 🔐 Bonnes pratiques de sécurité

### ✅ Recommandations pour la production

```yaml
# ✅ BON: Utiliser les clés SSH en production
hosts:
  prod_server:
    ssh_address: 10.0.0.50
    ssh_port: 22
    ssh_user: deploy
    ssh_key_file: ~/.ssh/id_rsa    # Clé SSH (plus sécurisé)
```

```yaml
# ⚠️  À ÉVITER: Authentification par mot de passe en production
hosts:
  dev_server:
    ssh_address: 192.168.1.20
    ssh_user: ubuntu
    ssh_password: "secret"          # Seulement pour les tests!
```

### Bonnes pratiques

- ✅ Utiliser les clés SSH pour les serveurs de production
- ✅ Toujours utiliser `--dry-run` avant l'exécution réelle
- ✅ Réviser les playbooks avant de les exécuter en production
- ✅ Restreindre l'accès SSH aux adresses IP autorisées
- ✅ Utiliser des passphrases fortes pour les clés SSH
- ✅ Stocker les identifiants dans des variables d'environnement

---

## 🆘 Dépannage

### Problème: "Timeout de connexion SSH"

```bash
# Vérifier si le serveur est accessible
ping <host_ip>

# Tester la connexion SSH
ssh -p 22 <user>@<host_ip>

# Vérifier la configuration de l'inventory
cat inventory.yml
```

### Problème: "Module apt non trouvé"

```bash
# Réinstaller le package
pip install -e .

# Vérifier que les modules existent
ls -la mylittleansible/modules/
```

### Problème: "Permission refusée"

```bash
# Vérifier les permissions de la clé SSH
chmod 600 ~/.ssh/id_rsa

# Vérifier que l'utilisateur a les permissions
ssh -i ~/.ssh/id_rsa user@host "sudo -l"
```

### Problème: "Le dry-run donne une erreur"

Utilisez `--debug` pour voir la stack trace complète:

```bash
mla -f playbook.yml -i inventory.yml --dry-run --debug
```

---

## 📚 Dépendances

| Package | Version | Objectif |
|---|---|---|
| **paramiko** | 3.4.0+ | Protocole SSH |
| **jinja2** | 3.1.2+ | Rendu de templates |
| **click** | 8.1.7+ | Framework CLI |
| **pyyaml** | 6.0.1+ | Parsing YAML |

### Installer toutes les dépendances

```bash
pip install -r requirements.txt
```

---

## 🎓 Parcours d'apprentissage

1. **Comprendre les concepts IaC** - Lire l'aperçu ci-dessus
2. **Essayer le dry-run** - `mla -f examples/playbooks/test_apt.yml -i examples/inventory/inventory.yml --dry-run`
3. **Créer un inventory** - Définir vos serveurs cibles
4. **Écrire un playbook** - Définir vos tâches
5. **Tester avec dry-run** - Aperçu avant exécution
6. **Exécuter** - Lancer le playbook
7. **Surveiller la sortie** - Vérifier les logs pour le statut

---

## 🚀 Checklist de déploiement en production

- [ ] Toutes les tâches testées avec `--dry-run`
- [ ] Clés SSH configurées pour tous les hôtes
- [ ] Playbook revu par l'équipe
- [ ] Sauvegarde des configurations critiques créée
- [ ] Plan de rollback documenté
- [ ] Monitoring/logging en place
- [ ] Exécuter le playbook en heures creuses
- [ ] Vérifier que toutes les tâches ont réussi

---

## 📈 Historique des versions

**v1.0.0** (Actuel - Jan 13, 2026)
- ✅ 6 modules entièrement implémentés
- ✅ Mode dry-run (aperçu des changements)
- ✅ Mode debug (stack traces)
- ✅ Niveaux de verbosité (-v, -vv, -vvv)
- ✅ Authentification par clé SSH
- ✅ Support des templates Jinja2
- ✅ Garantie d'idempotence
- ✅ Logging professionnel
- ✅ Conforme 100% PEP8

---

## 🤝 Contribution

Les contributions sont bienvenues! Pour ajouter des fonctionnalités:

1. Créer une branche de fonctionnalité
2. Implémenter avec tests
3. Exécuter `pytest` pour vérifier
4. Assurer la conformité PEP8
5. Soumettre une pull request

---

## 📄 Licence

À des fins éducatives et d'apprentissage.

---

## 🎯 Comparaison avec Ansible

| Aspect | MyLittleAnsible | Ansible |
|---|---|---|
| **Modules** | 6 core | 100+ |
| **Temps d'apprentissage** | 30 minutes | 2+ jours |
| **Setup** | pip install | Complexe |
| **Playbooks YAML** | Oui | Oui |
| **Inventory** | Simple | Complexe |
| **Communauté** | Éducatif | Enterprise |

**MyLittleAnsible = Les concepts clés d'Ansible, simplifiés!**

---

## 🔥 Fonctionnalités principales

### 🎯 Mode Dry-Run

Aperçu de tous les changements avant exécution:

```bash
mla -f playbook.yml -i inventory.yml --dry-run
# Montre exactement ce qui se passera, ne change rien!
```

### 🐛 Mode Debug

Détails d'erreur complets pour le dépannage:

```bash
mla -f playbook.yml -i inventory.yml --debug
# Affiche la stack trace complète en cas d'erreur
```

### 🔄 Idempotence

Exécuter le même playbook plusieurs fois en toute sécurité. Deuxième exécution = aucun changement:

```bash
# Première exécution: installe nginx
mla -f playbook.yml -i inventory.yml
# [OK] apt [CHANGED]

# Deuxième exécution: nginx existe déjà
mla -f playbook.yml -i inventory.yml
# [OK] apt (inchangé)
```

---

## 📞 Support

Vous avez des problèmes? Vérifiez:
1. **Sortie du dry-run** - Utilisez `--dry-run` pour tester d'abord
2. **Logs de debug** - Utilisez `--debug` pour les détails complets
3. **Configuration de l'inventory** - Vérifiez les identifiants SSH
4. **Connectivité SSH** - Testez avec `ssh user@host`
5. **Sortie verbose** - Utilisez `-vvv` pour le maximum de détails

---

## ⭐ Conseils pro

```bash
# Toujours tester d'abord avec dry-run
mla -f playbook.yml -i inventory.yml --dry-run

# Utiliser la sortie verbose lors du dépannage
mla -f playbook.yml -i inventory.yml -vvv

# Combiner dry-run + verbose + debug
mla -f playbook.yml -i inventory.yml --dry-run -vvv --debug

# Vérifier votre inventory avant d'exécuter
mla --version  # Vérifier que c'est correctement installé
```

---

## 🎉 C'est parti!

```bash
# 1. Installer
pip install -e .

# 2. Vérifier que ça fonctionne
mla --help

# 3. Créer inventory.yml

# 4. Créer playbook.yml

# 5. Tester avec dry-run
mla -f playbook.yml -i inventory.yml --dry-run

# 6. Exécuter
mla -f playbook.yml -i inventory.yml

# 7. Célébrer! 🎊
```

---

**Heureux d'automatiser!** 🚀

---

**Dernière mise à jour:** 13 janvier 2026  
**Version:** 1.0.0  
**Status:** ✅ Prêt pour la production
