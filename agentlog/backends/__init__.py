"""Storage backends for AgentLog."""

from agentlog.backends.local import LocalBackend
from agentlog.backends.supabase import SupabaseBackend

__all__ = ["LocalBackend", "SupabaseBackend"]
