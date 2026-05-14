from contextlib import contextmanager
from typing import Iterator

import psycopg
from psycopg.rows import dict_row

from api.config import get_settings


@contextmanager
def get_db_cursor() -> Iterator[psycopg.Cursor]:
    settings = get_settings()
    with psycopg.connect(settings.database_url, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            yield cur
        conn.commit()


def db_ping() -> bool:
    settings = get_settings()
    try:
        with psycopg.connect(settings.database_url) as conn:
            with conn.cursor() as cur:
                cur.execute("select 1")
                cur.fetchone()
        return True
    except Exception:
        return False
