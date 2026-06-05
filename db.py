
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable
import duckdb

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "data" / "fridgemate.duckdb"
SCHEMA_PATH = ROOT / "schema.sql"
SEED_PATH = ROOT / "seed.sql"

def connect() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH))

def initialize_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with connect() as con:
        con.execute(SCHEMA_PATH.read_text(encoding="utf-8"))
        con.execute(SEED_PATH.read_text(encoding="utf-8"))

def next_id(con: duckdb.DuckDBPyConnection, table: str, column: str) -> int:
    value = con.execute(
        f"SELECT COALESCE(MAX({column}), 0) + 1 FROM {table}"
    ).fetchone()[0]
    return int(value)

def rows_as_dicts(cursor: duckdb.DuckDBPyConnection) -> list[dict[str, Any]]:
    columns = [d[0] for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
