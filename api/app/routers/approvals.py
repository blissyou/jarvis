from __future__ import annotations

from fastapi import APIRouter, HTTPException

from api.app.persistence import db
from api.app.schemas.contracts import ApprovalDecisionOut, ApprovalOut, TurnOut
from api.app.services.tools import get_tool, invoke_tool

router = APIRouter(prefix="/approvals", tags=["approvals"])


@router.post("/{approval_id}/approve", response_model=ApprovalDecisionOut)
def approve(approval_id: str) -> ApprovalDecisionOut:
    approval = db.get_approval(approval_id)
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    if approval["status"] != "pending":
        raise HTTPException(status_code=409, detail="Approval is already resolved")

    preview = db.approval_to_dict(approval)["preview"]
    tool_name = preview.get("tool_name")
    args = preview.get("arguments", {})
    manifest = get_tool(tool_name)
    if manifest is None:
        raise HTTPException(status_code=400, detail="Unknown approved tool")

    result = invoke_tool(tool_name, args)
    resolved = db.resolve_approval(approval_id, "approved")
    assert resolved is not None
    turn = db.update_turn_status(approval["turn_id"], "completed" if result.status == "succeeded" else result.status, f"Approved action completed: {result.summary}")
    db.insert_tool_invocation(approval["session_id"], approval["turn_id"], tool_name, manifest.risk_class.value, result.status, result.changed_state, result.model_dump())
    db.insert_event(approval["session_id"], approval["turn_id"], "approval_resolved", approval["risk_level"], {"status": "approved"})
    db.insert_event(approval["session_id"], approval["turn_id"], "tool_call", approval["risk_level"], result.model_dump())
    return ApprovalDecisionOut(approval=ApprovalOut(**db.approval_to_dict(resolved)), turn=TurnOut(**db.turn_to_dict(turn)) if turn else None)


@router.post("/{approval_id}/reject", response_model=ApprovalDecisionOut)
def reject(approval_id: str) -> ApprovalDecisionOut:
    approval = db.get_approval(approval_id)
    if approval is None:
        raise HTTPException(status_code=404, detail="Approval not found")
    if approval["status"] != "pending":
        raise HTTPException(status_code=409, detail="Approval is already resolved")

    resolved = db.resolve_approval(approval_id, "rejected")
    assert resolved is not None
    turn = db.update_turn_status(approval["turn_id"], "rejected", "The user rejected the requested action. No state changed.")
    db.insert_event(approval["session_id"], approval["turn_id"], "approval_resolved", approval["risk_level"], {"status": "rejected"})
    return ApprovalDecisionOut(approval=ApprovalOut(**db.approval_to_dict(resolved)), turn=TurnOut(**db.turn_to_dict(turn)) if turn else None)
