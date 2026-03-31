"""Supabase backend — optional cloud storage for agent events."""

from __future__ import annotations

from typing import Any, Dict

from agentlog.schema import AgentEvent


class SupabaseBackend:
    """Persist events to a Supabase table (``agent_events``).

    The ``supabase`` package is imported lazily so the core SDK
    stays dependency-free. Install the extra with::

        pip install auditlog-ai[supabase]
    """

    def __init__(self, url: str, key: str) -> None:
        self.url = url
        self.key = key
        self._client: Any = None

    def _get_client(self) -> Any:
        """Lazily initialise the Supabase client."""
        if self._client is None:
            try:
                from supabase import create_client
            except ImportError:
                raise ImportError(
                    "The supabase package is required for SupabaseBackend. "
                    "Install it with: pip install auditlog-ai[supabase]"
                )
            self._client = create_client(self.url, self.key)
        return self._client

    def save(self, event: AgentEvent) -> Dict[str, Any]:
        """Insert a single event into the ``agent_events`` table."""
        client = self._get_client()
        response = client.table("agent_events").insert(event.to_dict()).execute()
        return response.data
