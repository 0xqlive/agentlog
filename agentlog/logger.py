"""AgentLogger — the main interface for recording agent actions."""

from __future__ import annotations

import time
import uuid
from typing import Any, Optional

from agentlog.backends.local import LocalBackend
from agentlog.schema import AgentEvent


class AgentLogger:
    """High-level logger that creates and persists AgentEvent records.

    Can be used directly via :meth:`log`, or as a context manager
    for automatic timing and logging on exit.

    Examples
    --------
    Direct call::

        logger = AgentLogger(agent_id="my-agent", model_id="gpt-4")
        event = logger.log(input_text="Hello", output_text="Hi there")

    Context manager::

        with AgentLogger(agent_id="my-agent", model_id="gpt-4") as logger:
            result = call_model(prompt)
            logger.set_output(result)
    """

    def __init__(
        self,
        agent_id: str,
        session_id: Optional[str] = None,
        backend: Optional[Any] = None,
        model_id: str = "unknown",
    ) -> None:
        self.agent_id = agent_id
        self.session_id = session_id or str(uuid.uuid4())
        self.backend = backend or LocalBackend()
        self.model_id = model_id

        # Context-manager state
        self._start_time: Optional[float] = None
        self._input_text: Optional[str] = None
        self._output_text: Optional[str] = None

    # ------------------------------------------------------------------
    # Core API
    # ------------------------------------------------------------------

    def log(
        self,
        input_text: str,
        output_text: str,
        **kwargs: Any,
    ) -> AgentEvent:
        """Create an event from raw strings, persist it, and return it."""
        event = AgentEvent.from_call(
            agent_id=self.agent_id,
            session_id=self.session_id,
            input_text=input_text,
            output_text=output_text,
            model_id=self.model_id,
            **kwargs,
        )
        self.backend.save(event)
        return event

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def set_output(self, output_text: str) -> None:
        """Store the output so it is logged automatically on ``__exit__``."""
        self._output_text = output_text

    def __enter__(self) -> AgentLogger:
        self._start_time = time.monotonic()
        self._output_text = None
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        if self._output_text is not None:
            latency_ms = None
            if self._start_time is not None:
                latency_ms = int((time.monotonic() - self._start_time) * 1000)
            self.log(
                input_text=self._input_text or "",
                output_text=self._output_text,
                latency_ms=latency_ms,
            )
        self._start_time = None
        self._output_text = None
