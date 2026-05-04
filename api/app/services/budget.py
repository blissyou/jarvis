from __future__ import annotations

import os

from api.app.persistence.db import budget_summary
from api.app.schemas.contracts import BudgetOut


def current_budget() -> BudgetOut:
    monthly = int(os.getenv("JARVIS_BUDGET_MONTHLY_KRW", "10000"))
    return BudgetOut(**budget_summary(monthly))
