"""Local JSONL file backend — zero dependencies, works everywhere."""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List

from agentlog.schema import AgentEvent


class LocalBackend:
    """Append-only JSONL backend stored on the local filesystem.

    Each event is one JSON line, making it trivial to stream,
    grep, or pipe into any downstream tool.
    """

    def __init__(self, filepath: str = "agentlog.jsonl") -> None:
        self.filepath = filepath

    def save(self, event: AgentEvent) -> None:
        """Append a single event as a JSON line."""
        with open(self.filepath, "a", encoding="utf-8") as f:
            f.write(event.to_json() + "\n")

    def read_all(self) -> List[Dict[str, Any]]:
        """Read every event from the file and return a list of dicts."""
        if not os.path.exists(self.filepath):
            return []
        with open(self.filepath, "r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def clear(self) -> None:
        """Delete the log file entirely."""
        if os.path.exists(self.filepath):
            os.remove(self.filepath)
