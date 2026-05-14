"""Smoke-check that Phase 1 tables exist in PostgreSQL."""

import sys

import psycopg

from api.config import get_settings

REQUIRED_TABLES = {
    "organizations",
    "organization_members",
    "projects",
    "apps",
    "workflow_events",
    "idempotency_records",
}


def main() -> int:
    settings = get_settings()
    with psycopg.connect(settings.database_url) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select table_name
                from information_schema.tables
                where table_schema = 'public'
                """
            )
            existing = {row[0] for row in cur.fetchall()}

    missing = sorted(REQUIRED_TABLES - existing)
    if missing:
        print("Missing tables:", ", ".join(missing))
        return 1
    print("Schema check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
