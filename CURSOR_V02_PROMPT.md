# Prompt Cursor — Push v0.2 et publish sur PyPI

## 1. Vérifier que les nouveaux fichiers existent

Ces fichiers doivent être présents :
- `agentlog/async_logger.py`
- `agentlog/backends/async_local.py`
- `agentlog/backends/postgres.py`

Si l'un d'entre eux manque, stop et signale-le.

## 2. Vérifier pyproject.toml

Le fichier doit contenir :
- `name = "auditlog-ai"`
- `version = "0.2.0"`
- Optional deps :
  - `supabase = ["supabase>=2.0.0"]`
  - `postgres = ["psycopg2-binary>=2.9.0"]`
  - `async = ["aiofiles>=23.0.0"]`
  - `all = ["supabase>=2.0.0", "psycopg2-binary>=2.9.0", "aiofiles>=23.0.0"]`

Si les optional deps `postgres`, `async`, ou `all` manquent, ajoute-les.

## 3. Test rapide

Lance :
```bash
python -c "from agentlog import AgentLogger, AsyncAgentLogger, AgentEvent, log_agent, alog_agent, LocalBackend, SupabaseBackend, PostgresBackend, AsyncLocalBackend; print('All imports OK — v' + __import__('agentlog').__version__)"
```

Ça doit afficher `All imports OK — v0.2.0`. Si ça échoue, fix l'erreur.

## 4. Git commit et push

```bash
git add -A
git commit -m "feat: v0.2.0 — async support, PostgreSQL backend, raw content storage"
git push origin main
```

## 5. Build et publish sur PyPI

```bash
rm -rf dist/ build/ *.egg-info
python -m build
source .env
twine upload dist/* --username __token__ --password "$TWINE_TOKEN"
```

Ou si publish.sh existe :
```bash
rm -rf dist/ build/ *.egg-info
python -m build
./publish.sh
```

## 6. Vérification finale

Affiche le lien PyPI : https://pypi.org/project/auditlog-ai/0.2.0/

## Ce qu'il ne faut PAS faire

- Ne modifie pas le code des fichiers existants (sauf pyproject.toml si les deps manquent)
- Ne crée pas de nouveaux fichiers
- Ne change pas les imports ou la logique
- Ne touche pas à `.env`
