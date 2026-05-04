from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.app.persistence import db
from api.app.schemas.contracts import EventOut, PlanStep, SessionCreate, SessionOut, TurnCreate, TurnOut
from api.app.security.policy import requires_approval, risk_level_for
from api.app.services.model_router import router as model_router
from api.app.services.tools import choose_tool, get_tool, invoke_tool

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.post("", response_model=SessionOut)
def create_session(payload: SessionCreate) -> SessionOut:
    row = db.create_session(payload.workspace_root)
    db.insert_event(row["id"], None, "session_created", None, {"workspace_root": payload.workspace_root})
    return SessionOut(**db.session_to_dict(row))


@router.get("/{session_id}/events", response_model=list[EventOut])
def get_events(session_id: str) -> list[EventOut]:
    if db.get_session(session_id) is None:
        raise HTTPException(status_code=404, detail="Session not found")
    return [EventOut(**event) for event in db.list_events(session_id)]


@router.post("/{session_id}/turns", response_model=TurnOut)
def create_turn(session_id: str, payload: TurnCreate) -> TurnOut:
    session = db.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found")

    workspace_root = payload.workspace.cwd or session["workspace_root"]
    user_text = payload.input.text
    tool_name, args = choose_tool(user_text, workspace_root=workspace_root, selected_files=payload.workspace.selected_files)
    model_reply = model_router.infer(user_text, sensitive=bool(payload.workspace.selected_files), cloud_allowed=payload.policy.cloud_allowed)

    if tool_name is None:
        plan = [PlanStep(step_id="step_chat", kind="chat", arguments={}).model_dump()]
        turn = db.insert_turn(
            session_id=session_id,
            input_mode=payload.input.mode.value,
            user_text=user_text,
            mode="chat",
            risk_level="low",
            requires_approval=False,
            status="completed",
            plan=plan,
            final_response=model_reply.text,
        )
        db.insert_model_call(session_id, turn["id"], model_reply.route.provider, model_reply.route.route_reason, model_reply.route.estimated_cost_krw)
        db.insert_event(session_id, turn["id"], "model_call", "low", model_reply.route.__dict__)
        db.insert_event(session_id, turn["id"], "turn_completed", "low", {"mode": "chat"})
        return TurnOut(**db.turn_to_dict(turn))

    manifest = get_tool(tool_name)
    if manifest is None:
        raise HTTPException(status_code=400, detail="Unknown tool selected")

    approval_needed = manifest.requires_approval or requires_approval(manifest.risk_class, path=args.get("path"), workspace_root=workspace_root)
    risk = risk_level_for(manifest.risk_class)
    plan = [PlanStep(step_id="step_tool_1", kind="tool", tool=tool_name, arguments=args).model_dump()]

    if approval_needed:
        turn = db.insert_turn(
            session_id=session_id,
            input_mode=payload.input.mode.value,
            user_text=user_text,
            mode="tool",
            risk_level=risk,
            requires_approval=True,
            status="awaiting_approval",
            plan=plan,
            final_response="This action needs approval before execution.",
        )
        approval = db.create_approval(
            session_id=session_id,
            turn_id=turn["id"],
            risk_level=risk,
            action_summary=f"Run {tool_name}",
            preview={"tool_name": tool_name, "arguments": args, "risk_class": manifest.risk_class.value},
        )
        db.update_turn_approval(turn["id"], approval["id"])
        updated = db.get_turn(turn["id"])
        assert updated is not None
        db.insert_model_call(session_id, turn["id"], model_reply.route.provider, model_reply.route.route_reason, model_reply.route.estimated_cost_krw)
        db.insert_event(session_id, turn["id"], "approval_requested", risk, db.approval_to_dict(approval))
        return TurnOut(**db.turn_to_dict(updated))

    result = invoke_tool(tool_name, args, workspace_root=workspace_root)
    final_response = f"{model_reply.text}\n\nTool result: {result.summary}"
    turn = db.insert_turn(
        session_id=session_id,
        input_mode=payload.input.mode.value,
        user_text=user_text,
        mode="tool",
        risk_level=risk,
        requires_approval=False,
        status="completed" if result.status == "succeeded" else result.status,
        plan=plan,
        final_response=final_response,
    )
    db.insert_model_call(session_id, turn["id"], model_reply.route.provider, model_reply.route.route_reason, model_reply.route.estimated_cost_krw)
    db.insert_tool_invocation(session_id, turn["id"], tool_name, manifest.risk_class.value, result.status, result.changed_state, result.model_dump())
    db.insert_event(session_id, turn["id"], "tool_call", risk, result.model_dump())
    db.insert_event(session_id, turn["id"], "turn_completed", risk, {"mode": "tool", "tool": tool_name})
    return TurnOut(**db.turn_to_dict(turn))
