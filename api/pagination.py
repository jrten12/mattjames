from __future__ import annotations

import base64
from datetime import datetime
from uuid import UUID


def encode_cursor(created_at: datetime, entity_id: UUID) -> str:
    payload = f"{created_at.isoformat()}|{entity_id}"
    return base64.urlsafe_b64encode(payload.encode("utf-8")).decode("ascii")


def decode_cursor(cursor: str) -> tuple[datetime, UUID] | None:
    try:
        raw = base64.urlsafe_b64decode(cursor.encode("ascii")).decode("utf-8")
        created_at_raw, entity_id_raw = raw.split("|", maxsplit=1)
        created_at = datetime.fromisoformat(created_at_raw)
        entity_id = UUID(entity_id_raw)
        return created_at, entity_id
    except Exception:
        return None
