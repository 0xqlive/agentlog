"""Async local JSONL file backend — async file I/O with aiofiles."""

from __future__ import annotations

from typing import Any, Dict, List

from agentlog.schema import AgentEvent


class AsyncLocalBackend:
    """Async append-only JSONL backend stored on the local filesystem.

    Uses aiofiles for non-blocking file I/O. The ``aiofiles`` package
    is imported lazily so the core SDK stays dependency-free.
    Install the extra with::

        pip install auditlog-ai[async]
    """

    def __init__(self, filepath: str = "agentlog.jsonl") -> None:
        self.filepath = filepath

    async def async_save(self, event: AgentEvent) -> None:
        """Append a single event as a JSON line using async I/O."""
        try:
            import aiofiles
        except ImportError:
            raise ImportError(
                "The aiofiles package is required for AsyncLocalBackend. "
                "Install it with: pip install auditlog-ai[async]"
            )

        async with aiofiles.open(self.filepath, "a", encoding="utf-8") as f:
            await f.write(event.to_json() + "\n")

    async def read_all(self) -> List[Dict[str, Any]]:
        """Read every event from the file and return a list of dicts asynchronously."""
        try:
            import aiofiles
        except ImportError:
            raise ImportError(
                "The aiofiles package is required for AsyncLocalBackend. "
                "Install it with: pip install auditlog-ai[async]"
            )

        import json
        import os

        if not os.path.exists(self.filepath):
            return []

        async with aiofiles.open(self.filepath, "r", encoding="utf-8") as f:
            content = await f.read()
            return [json.loads(line) for line in content.split("\n") if line.strip()]

    async def clear(self) -> None:
        """Delete the log file entirely."""
        try:
            import aiofiles
        except ImportError:
            raise ImportError(
                "The aiofiles package is required for AsyncLocalBackend. "
                "Install it with: pip install auditlog-ai[async]"
            )

        import os

        if os.path.exists(self.filepath):
            os.remove(self.filepath)
