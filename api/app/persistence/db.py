from __future__ import annotations

import json
import os
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator

DATA_DIR = Path(os.getenv("JARVIS_DATA_DIR", "runtime"))
DB_PATH = DATA_DIR / "db" / "jarvis.sqlite3"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:16]}"


def _json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False)


def _loads(text: str | None) -> Any:
    if not text:
        return None
    return json.loads(text)


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with connect() as conn:
        conn.executescript(
            """
            create table if not exists sessions (
              id text primary key,
              created_at text not null,
              workspace_root text,
              status text not null
            );

            create table if not exists turns (
              id text primary key,
              session_id text not null references sessions(id),
              input_mode text not null,
              user_text text not null,
              mode text not null,
              risk_level text not null,
              requires_approval integer not null,
              status text not null,
              plan_json text not null,
              final_response text,
              approval_id text,
              created_at text not null
            );

            create table if not exists approvals (
              id text primary key,
              session_id text not null references sessions(id),
              turn_id text references turns(id),
              risk_level text not null,
              action_summary text not null,
              status text not null,
              preview_json text not null,
              created_at text not null,
              resolved_at text
            );

            create table if not exists events (
              id text primary key,
              session_id text not null,
              turn_id text,
              event_type text not null,
              risk_level text,
              payload_json text not null,
              created_at text not null
            );

            create table if not exists tool_invocations (
              id text primary key,
              session_id text not null,
              turn_id text,
              tool_name text not null,
              risk_class text not null,
              status text not null,
              changed_state integer not null,
              result_json text not null,
              created_at text not null
            );

            create table if not exists model_calls (
              id text primary key,
              session_id text not null,
              turn_id text,
              provider text not null,
              route_reason text not null,
              estimated_cost_krw real not null,
              created_at text not null
            );
            """
        )


def create_session(workspace_root: str | None) -> sqlite3.Row:
    session_id = new_id("sess")
    with connect() as conn:
        conn.execute(
            "insert into sessions (id, created_at, workspace_root, status) values (?, ?, ?, ?)",
            (session_id, utc_now(), workspace_root, "active"),
        )
        row = conn.execute("select * from sessions where id = ?", (session_id,)).fetchone()
        assert row is not None
        return row


def get_session(session_id: str) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute("select * from sessions where id = ?", (session_id,)).fetchone()


def list_events(session_id: str) -> list[dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute(
            "select * from events where session_id = ? order by created_at asc", (session_id,)
        ).fetchall()
    return [event_to_dict(r) for r in rows]


def insert_event(session_id: str, turn_id: str | None, event_type: str, risk_level: str | None, payload: dict[str, Any]) -> None:
    with connect() as conn:
        conn.execute(
            "insert into events (id, session_id, turn_id, event_type, risk_level, payload_json, created_at) values (?, ?, ?, ?, ?, ?, ?)",
            (new_id("evt"), session_id, turn_id, event_type, risk_level, _json(payload), utc_now()),
        )


def insert_turn(
    session_id: str,
    input_mode: str,
    user_text: str,
    mode: str,
    risk_level: str,
    requires_approval: bool,
    status: str,
    plan: list[dict[str, Any]],
    final_response: str | None,
    approval_id: str | None = None,
) -> sqlite3.Row:
    turn_id = new_id("turn")
    with connect() as conn:
        conn.execute(
            """
            insert into turns
            (id, session_id, input_mode, user_text, mode, risk_level, requires_approval, status, plan_json, final_response, approval_id, created_at)
            values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                turn_id,
                session_id,
                input_mode,
                user_text,
                mode,
                risk_level,
                1 if requires_approval else 0,
                status,
                _json(plan),
                final_response,
                approval_id,
                utc_now(),
            ),
        )
        row = conn.execute("select * from turns where id = ?", (turn_id,)).fetchone()
        assert row is not None
        return row


def update_turn_approval(turn_id: str, approval_id: str) -> None:
    with connect() as conn:
        conn.execute("update turns set approval_id = ? where id = ?", (approval_id, turn_id))


def update_turn_status(turn_id: str, status: str, final_response: str | None = None) -> sqlite3.Row | None:
    with connect() as conn:
        conn.execute("update turns set status = ?, final_response = coalesce(?, final_response) where id = ?", (status, final_response, turn_id))
        return conn.execute("select * from turns where id = ?", (turn_id,)).fetchone()


def get_turn(turn_id: str) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute("select * from turns where id = ?", (turn_id,)).fetchone()


def create_approval(session_id: str, turn_id: str, risk_level: str, action_summary: str, preview: dict[str, Any]) -> sqlite3.Row:
    approval_id = new_id("appr")
    with connect() as conn:
        conn.execute(
            """
            insert into approvals (id, session_id, turn_id, risk_level, action_summary, status, preview_json, created_at)
            values (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (approval_id, session_id, turn_id, risk_level, action_summary, "pending", _json(preview), utc_now()),
        )
        row = conn.execute("select * from approvals where id = ?", (approval_id,)).fetchone()
        assert row is not None
        return row


def get_approval(approval_id: str) -> sqlite3.Row | None:
    with connect() as conn:
        return conn.execute("select * from approvals where id = ?", (approval_id,)).fetchone()


def resolve_approval(approval_id: str, status: str) -> sqlite3.Row | None:
    with connect() as conn:
        conn.execute("update approvals set status = ?, resolved_at = ? where id = ?", (status, utc_now(), approval_id))
        return conn.execute("select * from approvals where id = ?", (approval_id,)).fetchone()


def insert_tool_invocation(session_id: str, turn_id: str | None, tool_name: str, risk_class: str, status: str, changed_state: bool, result: dict[str, Any]) -> None:
    with connect() as conn:
        conn.execute(
            "insert into tool_invocations (id, session_id, turn_id, tool_name, risk_class, status, changed_state, result_json, created_at) values (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (new_id("tool"), session_id, turn_id, tool_name, risk_class, status, 1 if changed_state else 0, _json(result), utc_now()),
        )


def insert_model_call(session_id: str, turn_id: str | None, provider: str, route_reason: str, estimated_cost_krw: float) -> None:
    with connect() as conn:
        conn.execute(
            "insert into model_calls (id, session_id, turn_id, provider, route_reason, estimated_cost_krw, created_at) values (?, ?, ?, ?, ?, ?, ?)",
            (new_id("model"), session_id, turn_id, provider, route_reason, estimated_cost_krw, utc_now()),
        )


def budget_summary(monthly_budget_krw: int) -> dict[str, Any]:
    with connect() as conn:
        model = conn.execute("select provider, count(*) c, sum(estimated_cost_krw) cost from model_calls group by provider").fetchall()
        tool_calls = conn.execute("select count(*) c from tool_invocations").fetchone()["c"]
        approvals = conn.execute("select count(*) c from approvals").fetchone()["c"]
    cloud_calls = sum(r["c"] for r in model if r["provider"] not in {"ollama", "lmstudio", "local_echo"})
    local_calls = sum(r["c"] for r in model if r["provider"] in {"ollama", "lmstudio", "local_echo"})
    cost = sum(float(r["cost"] or 0) for r in model)
    return {
        "monthly_budget_krw": monthly_budget_krw,
        "estimated_cost_krw": cost,
        "cloud_model_calls": cloud_calls,
        "local_model_calls": local_calls,
        "tool_calls": tool_calls,
        "approval_requests": approvals,
    }


def session_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    return dict(row)


def turn_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    return {
        "id": data["id"],
        "session_id": data["session_id"],
        "mode": data["mode"],
        "risk_level": data["risk_level"],
        "requires_approval": bool(data["requires_approval"]),
        "status": data["status"],
        "plan": _loads(data["plan_json"]) or [],
        "final_response": data["final_response"],
        "approval_id": data["approval_id"],
    }


def approval_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    return {
        "id": data["id"],
        "session_id": data["session_id"],
        "turn_id": data["turn_id"],
        "risk_level": data["risk_level"],
        "action_summary": data["action_summary"],
        "status": data["status"],
        "preview": _loads(data["preview_json"]) or {},
        "created_at": data["created_at"],
        "resolved_at": data["resolved_at"],
    }


def event_to_dict(row: sqlite3.Row) -> dict[str, Any]:
    data = dict(row)
    return {
        "id": data["id"],
        "session_id": data["session_id"],
        "turn_id": data["turn_id"],
        "event_type": data["event_type"],
        "risk_level": data["risk_level"],
        "payload": _loads(data["payload_json"]) or {},
        "created_at": data["created_at"],
    }
