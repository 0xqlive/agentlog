"""AgentLog — automatic compliance logging for AI agents."""

from __future__ import annotations

import functools
from typing import Any, Callable, Optional

from agentlog.async_logger import AsyncAgentLogger
from agentlog.backends.async_local import AsyncLocalBackend
from agentlog.backends.local import LocalBackend
from agentlog.backends.postgres import PostgresBackend
from agentlog.backends.supabase import SupabaseBackend
from agentlog.logger import AgentLogger
from agentlog.schema import AgentEvent

__version__ = "0.2.0"

__all__ = [
    "AgentLogger",
    "AsyncAgentLogger",
    "AgentEvent",
    "log_agent",
    "alog_agent",
    "LocalBackend",
    "SupabaseBackend",
    "PostgresBackend",
    "AsyncLocalBackend",
]


def log_agent(
    func: Optional[Callable[..., Any]] = None,
    *,
    agent_id: str = "default",
    model_id: str = "unknown",
    backend: Optional[Any] = None,
) -> Any:
    """Decorator that wraps a function and logs every call automatically.

    Can be used with or without arguments::

        @log_agent
        def ask(prompt: str) -> str: ...

        @log_agent(agent_id="my-bot", model_id="gpt-4")
        def ask(prompt: str) -> str: ...

    The decorated function's positional args are stringified as
    ``input_text`` and its return value as ``output_text``.
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        logger = AgentLogger(
            agent_id=agent_id,
            model_id=model_id,
            backend=backend or LocalBackend(),
        )

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = fn(*args, **kwargs)
            logger.log(
                input_text=str(args),
                output_text=str(result),
            )
            return result

        return wrapper

    # Support both @log_agent and @log_agent(...)
    if func is not None:
        return decorator(func)
    return decorator


def alog_agent(
    func: Optional[Callable[..., Any]] = None,
    *,
    agent_id: str = "default",
    model_id: str = "unknown",
    backend: Optional[Any] = None,
) -> Any:
    """Async decorator that wraps an async function and logs every call automatically.

    Can be used with or without arguments::

        @alog_agent
        async def ask(prompt: str) -> str: ...

        @alog_agent(agent_id="my-bot", model_id="gpt-4")
        async def ask(prompt: str) -> str: ...

    The decorated function's positional args are stringified as
    ``input_text`` and its return value as ``output_text``.
    """

    def decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
        logger = AsyncAgentLogger(
            agent_id=agent_id,
            model_id=model_id,
            backend=backend or LocalBackend(),
        )

        @functools.wraps(fn)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await fn(*args, **kwargs)
            await logger.log(
                input_text=str(args),
                output_text=str(result),
            )
            return result

        return wrapper

    # Support both @alog_agent and @alog_agent(...)
    if func is not None:
        return decorator(func)
    return decorator
