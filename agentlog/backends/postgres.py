"""PostgreSQL backend — optional database storage for agent events."""

from __future__ import annotations

from typing import Any, Dict, List

from agentlog.schema import AgentEvent


class PostgresBackend:
    """Persist events to a PostgreSQL database (``agent_events`` table).

    The ``psycopg2`` package is imported lazily so the core SDK
    stays dependency-free. Install the extra with::

        pip install auditlog-ai[postgres]
    """

    def __init__(self, dsn: str) -> None:
        """Initialize the PostgreSQL backend.

        Parameters
        ----------
        dsn : str
            PostgreSQL connection string (Data Source Name).
            Example: "postgresql://user:password@localhost:5432/dbname"
        """
        self.dsn = dsn
        self._connection: Any = None

    def _get_connection(self) -> Any:
        """Lazily initialise the PostgreSQL connection."""
        if self._connection is None:
            try:
                import psycopg2
            except ImportError:
                raise ImportError(
                    "The psycopg2 package is required for PostgresBackend. "
                    "Install it with: pip install auditlog-ai[postgres]"
                )
            self._connection = psycopg2.connect(self.dsn)
        return self._connection

    def save(self, event: AgentEvent) -> Dict[str, Any]:
        """Insert a single event into the ``agent_events`` table.

        Parameters
        ----------
        event : AgentEvent
            The event to persist.

        Returns
        -------
        Dict[str, Any]
            A dictionary with the inserted event data and ID if available.
        """
        connection = self._get_connection()
        cursor = connection.cursor()

        try:
            # Prepare the event data
            event_dict = event.to_dict()

            # Build the INSERT statement dynamically from the event dict
            columns = ", ".join(event_dict.keys())
            placeholders = ", ".join(["%s"] * len(event_dict))
            values = tuple(event_dict.values())

            query = (
                f"INSERT INTO agent_events ({columns}) VALUES ({placeholders}) "
                "RETURNING *;"
            )

            cursor.execute(query, values)
            result = cursor.fetchone()
            connection.commit()

            # Return the result as a dict (assumes column names match event dict keys)
            if result:
                col_names = [desc[0] for desc in cursor.description]
                return dict(zip(col_names, result))
            return event_dict

        finally:
            cursor.close()

    def read_all(self) -> List[Dict[str, Any]]:
        """Read all events from the ``agent_events`` table.

        Returns
        -------
        List[Dict[str, Any]]
            A list of all events as dictionaries.
        """
        connection = self._get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT * FROM agent_events ORDER BY timestamp;")
            rows = cursor.fetchall()

            if not rows:
                return []

            col_names = [desc[0] for desc in cursor.description]
            return [dict(zip(col_names, row)) for row in rows]

        finally:
            cursor.close()

    def close(self) -> None:
        """Close the database connection."""
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def __del__(self) -> None:
        """Ensure connection is closed on garbage collection."""
        self.close()
