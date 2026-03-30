# Launch checklist — dans l'ordre exact

## Étape 1 : Remplacer qlive-ai

Chercher-remplacer dans SHOW_HN.md et ce fichier avant toute autre action.

## Étape 2 : PyPI d'abord (pour que le badge marche au push GitHub)

```bash
cd /path/to/agentlog

# Installer les outils de build
pip install build twine

# Build
python -m build

# Upload sur PyPI
# Créer un compte sur https://pypi.org si pas encore fait
# Créer un API token sur https://pypi.org/manage/account/token/
twine upload dist/*
# Username: __token__
# Password: pypi-xxxxxxxxxxxxxxxx (ton API token)
```

Vérifier que ça marche :

```bash
pip install agentlog
python -c "from agentlog import log_agent; print('OK')"
```

## Étape 3 : Décommenter le badge PyPI dans README.md

Retirer les `<!-- -->` autour du badge PyPI dans le README maintenant que le package est publié.

## Étape 4 : GitHub push

```bash
cd /path/to/agentlog

git init
git add .
git commit -m "Initial commit — AgentLog v0.1.0"

# Avec gh CLI (recommandé) :
gh repo create agentlog --public \
  --description "Audit trail for AI agents. One decorator, zero dependencies." \
  --source=. --push

# Ou manuellement : créer le repo sur github.com puis :
git remote add origin git@github.com:qlive-ai/agentlog.git
git branch -M main
git push -u origin main
```

## Étape 5 : Hacker News — le lendemain matin

Aller sur https://news.ycombinator.com/submit

- Title : `Show HN: AgentLog – open source audit trail for AI agents`
- URL : `https://github.com/qlive-ai/agentlog`
- Laisser le champ text vide (HN ignore text si une URL est fournie)
- Poster le contenu de SHOW_HN.md en premier commentaire juste après

Timing : mardi ou mercredi, 9h-11h EST.
