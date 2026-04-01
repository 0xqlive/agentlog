# AgentLog

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![PyPI](https://img.shields.io/pypi/v/auditlog-ai.svg)](https://pypi.org/project/auditlog-ai/)

Audit trail for AI agents. One decorator, zero dependencies.

```
pip install auditlog-ai
```

## The problem

Your agents call models, execute tools, make decisions. If something goes wrong — or an auditor asks what happened — you have nothing. No logs, no trail, no proof.

AgentLog fixes that. Every agent action gets a structured event: who did what, when, which model, who authorized it. Append-only JSONL, SHA-256 hashed I/O, ready to ship to any backend.

## 30 seconds to production

**Decorator** — wrap any function, done:

```python
from agentlog import log_agent

@log_agent(agent_id="support-bot", model_id="gpt-4")
def answer(prompt: str) -> str:
    return call_my_model(prompt)

answer("How do I reset my password?")
# → agentlog.jsonl gets a new line
```

**Context manager** — when you need timing:

```python
from agentlog import AgentLogger

with AgentLogger(agent_id="support-bot", model_id="gpt-4") as logger:
    result = call_my_model("How do I reset my password?")
    logger.set_output(result)
# → logged with latency_ms
```

**Direct call** — full control:

```python
from agentlog import AgentLogger

logger = AgentLogger(agent_id="support-bot", model_id="gpt-4")
logger.log(input_text="Hello", output_text="Hi there")
```

## What gets logged

```json
{
  "event_id": "a1b2c3d4-...",
  "agent_id": "support-bot",
  "session_id": "e5f6g7h8-...",
  "timestamp": "2026-03-30T12:00:00+00:00",
  "input_hash": "2cf24b72...",
  "output_hash": "486ea46...",
  "model_id": "gpt-4",
  "authorized_by": "system",
  "latency_ms": 423
}
```

Inputs and outputs are SHA-256 hashed. The actual content never touches the log unless you opt in with `store_raw=True`.

## v0.2 — Async, PostgreSQL, raw storage

**Async support** — for async agents:

```python
from agentlog import alog_agent

@alog_agent(agent_id="async-bot", model_id="claude-3")
async def answer(prompt: str) -> str:
    return await call_my_model(prompt)
```

```
pip install auditlog-ai[async]
```

**Store raw content** — when you need the full text, not just hashes:

```python
logger.log(input_text="Hello", output_text="Hi there", store_raw=True)
# → input_raw and output_raw fields included in the event
```

## Bring your own backend

JSONL by default. Supabase, PostgreSQL, or build your own:

```python
from agentlog import AgentLogger, SupabaseBackend, PostgresBackend

# Supabase
backend = SupabaseBackend(url="https://xxx.supabase.co", key="your-key")

# PostgreSQL
backend = PostgresBackend(dsn="postgresql://user:pass@localhost/mydb")

logger = AgentLogger(agent_id="my-agent", model_id="gpt-4", backend=backend)
```

```
pip install auditlog-ai[supabase]
pip install auditlog-ai[postgres]
pip install auditlog-ai[all]        # everything
```

Writing your own backend is one method: `save(event: AgentEvent)`.

## Design decisions

- **Zero dependencies.** Core uses only the standard library. No vendor lock-in.
- **Hashed by default.** Input/output never stored in plaintext unless you opt in with `store_raw=True`.
- **Append-only JSONL.** Grep it, stream it, pipe it. No database required.
- **Vendor-agnostic.** Works with OpenAI, Anthropic, LangChain, your custom stack.
- **Async-native.** Full async support for non-blocking agent pipelines.

## License

MIT
