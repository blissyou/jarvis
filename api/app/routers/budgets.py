from fastapi import APIRouter

from api.app.schemas.contracts import BudgetOut
from api.app.services.budget import current_budget

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("/current", response_model=BudgetOut)
def get_current_budget() -> BudgetOut:
    return current_budget()
