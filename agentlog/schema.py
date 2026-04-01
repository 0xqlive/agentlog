"""AgentEvent schema — the canonical data structure for every logged agent action."""

from __future__ import annotations

import hashlib
import json
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id() -> str:
    return str(uuid.uuid4())


@dataclass
class AgentEvent:
    """A single auditable event produced by an AI agent.

    Every field is serialisable to JSON. Hashes are SHA-256 of raw
    input/output text so the payload itself never has to be stored
    in the log if privacy policy forbids it.
    """

    agent_id: str
    session_id: str
    input_hash: str
    output_hash: str
    model_id: str
    event_id: str = field(default_factory=_new_id)
    timestamp: str = field(default_factory=_utc_now)
    model_version: str = ""
    authorized_by: str = "system"
    policy_id: Optional[str] = None
    latency_ms: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    input_raw: Optional[str] = None
    output_raw: Optional[str] = None

    # ------------------------------------------------------------------
    # Factory
    # ------------------------------------------------------------------

    @classmethod
    def from_call(
        cls,
        agent_id: str,
        session_id: str,
        input_text: str,
        output_text: str,
        model_id: str,
        store_raw: bool = False,
        **kwargs: Any,
    ) -> AgentEvent:
        """Build an event from raw input/output strings.

        Text is hashed with SHA-256 so the log stays lightweight
        and avoids storing potentially sensitive payloads.

        Parameters
        ----------
        agent_id : str
            Identifier for the agent.
        session_id : str
            Identifier for the session.
        input_text : str
            Raw input text.
        output_text : str
            Raw output text.
        model_id : str
            Identifier for the model used.
        store_raw : bool, optional
            If True, store the raw input and output text in the event.
            Default is False to maintain privacy.
        **kwargs : Any
            Additional fields to include in the event.

        Returns
        -------
        AgentEvent
            The constructed event.
        """
        input_hash = hashlib.sha256(input_text.encode("utf-8")).hexdigest()
        output_hash = hashlib.sha256(output_text.encode("utf-8")).hexdigest()

        # Optionally store raw content
        if store_raw:
            kwargs["input_raw"] = input_text
            kwargs["output_raw"] = output_text

        return cls(
            agent_id=agent_id,
            session_id=session_id,
            input_hash=input_hash,
            output_hash=output_hash,
            model_id=model_id,
            **kwargs,
        )

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def to_dict(self) -> Dict[str, Any]:
        """Return all fields as a plain dictionary."""
        return asdict(self)

    def to_json(self) -> str:
        """Return the event as a compact JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)
