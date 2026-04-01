# Prompt Cursor — Synchroniser le repo GitHub

Le package a été renommé de `agent-audit` à `auditlog-ai` sur PyPI. Le repo GitHub est en retard. Mets tout à jour et push.

## Ce qu'il faut faire

1. Dans `pyproject.toml` : vérifie que le name est bien `auditlog-ai`, que les URLs pointent vers `github.com/0xqlive/agentlog`, et que la version est `0.1.0`.

2. Dans `README.md` : remplace toute occurrence de `agent-audit` par `auditlog-ai`. Le pip install doit être `pip install auditlog-ai`. Le badge PyPI doit pointer vers `https://pypi.org/project/auditlog-ai/`. Décommente le badge PyPI s'il est commenté — le package est maintenant live.

3. Dans `agentlog/backends/supabase.py` : le message d'erreur ImportError doit dire `pip install auditlog-ai[supabase]`, pas `agent-audit[supabase]`.

4. Dans `SHOW_HN.md` : remplace toute occurrence de `agent-audit` par `auditlog-ai`. Le pip install doit être `pip install auditlog-ai`.

5. Dans `LAUNCH_COMMANDS.md` : remplace toute occurrence de `agent-audit` par `auditlog-ai`.

6. Supprime les fichiers de build qui ne doivent pas être sur le repo : `dist/`, `build/`, `*.egg-info/`, `__pycache__/`. Vérifie que `.gitignore` contient bien ces patterns.

7. Git add, commit avec le message : `chore: rename PyPI package to auditlog-ai and clean up build artifacts`

8. Push sur origin main.

## Ce qu'il ne faut PAS faire

- Ne touche pas au code Python (schema.py, logger.py, __init__.py, backends/local.py). Le package d'import reste `agentlog`.
- Ne change pas la version.
- Ne crée pas de fichiers supplémentaires.
- Ne modifie pas la logique du code.
