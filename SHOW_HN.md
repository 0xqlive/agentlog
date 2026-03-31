**Title:**
Show HN: AgentLog – open source audit trail for AI agents

**URL:**
https://github.com/0xqlive/agentlog

**Text:**

AI agents are making real decisions — answering customers, triggering workflows, calling APIs. But there's no standard way to log what they did, which model they used, or who authorized the action.

AgentLog is a Python SDK that fixes this. One decorator on your function, and every call gets a structured event: agent ID, session, model, timestamp, SHA-256 hashed I/O, authorization. Appended to a local JSONL file by default. Zero external dependencies.

```python
from agentlog import log_agent

@log_agent(agent_id="support-bot", model_id="gpt-4")
def answer(prompt):
    return call_my_model(prompt)
```

That's it. Every call to `answer()` is now logged.

What it is NOT: a monitoring tool, an observability platform, or a SaaS dashboard. It's a logging primitive. Think of it as `structlog` but purpose-built for agent compliance.

Core is MIT, zero dependencies, Python 3.9+. Optional Supabase backend if you want cloud storage.

I built this because I've been talking to companies deploying agents in production, and every single one has the same question: "how do we prove to an auditor what our agent did?" Nobody had a good answer.

Code: https://github.com/0xqlive/agentlog
PyPI: `pip install auditlog-ai`

What would make you actually use this? What's the first thing you'd want in v0.2?
