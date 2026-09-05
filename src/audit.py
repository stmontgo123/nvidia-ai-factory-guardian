"""In-memory immutable-style audit helper for the demonstration."""

from __future__ import annotations

from models import AuditEvent


def append_event(
    events: list[AuditEvent],
    event_type: str,
    message: str,
    *,
    actor: str = "guardian",
    details: dict | None = None,
) -> list[AuditEvent]:
    """Return a new list with a new event appended.

    Returning a new list makes accidental mutation less likely in the simple PoC.
    A production design would use a durable append-only event store.
    """
    return [
        *events,
        AuditEvent(
            event_type=event_type,
            message=message,
            actor=actor,
            details=details or {},
        ),
    ]
