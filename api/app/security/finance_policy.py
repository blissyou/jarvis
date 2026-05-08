from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class FinancePolicyDecision:
    blocked: bool
    reason: str | None = None
    matched_terms: tuple[str, ...] = ()


# MVP policy from the latest docs: market information is read-only; money movement
# and trade execution are not merely approval-gated, they are out of scope.
TRANSACTION_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\b(pay|payment|transfer|remit|wire|send money|bill pay|checkout)\b", "payments_or_transfers"),
    (r"\b(buy|sell|order|trade|rebalance|invest|liquidate)\b.*\b(stock|stocks|crypto|coin|btc|eth|fx|forex|shares?)\b", "trade_execution"),
    (r"\b(stock|stocks|crypto|coin|btc|eth|fx|forex|shares?)\b.*\b(buy|sell|order|trade|rebalance|invest|liquidate)\b", "trade_execution"),
    (r"(결제|송금|이체|입금|출금|청구서\s*납부|계좌\s*이동)", "payments_or_transfers"),
    (r"(매수|매도|주문|거래|자동\s*매매|리밸런싱|투자\s*실행|청산)", "trade_execution"),
)

ALLOWED_READONLY_HINTS = (
    "조회",
    "브리핑",
    "요약",
    "뉴스",
    "가격",
    "시세",
    "quote",
    "brief",
    "summarize",
    "price",
    "news",
)


def evaluate_financial_transaction_policy(text: str) -> FinancePolicyDecision:
    normalized = re.sub(r"\s+", " ", text.strip().lower())
    matched: list[str] = []
    for pattern, label in TRANSACTION_PATTERNS:
        if re.search(pattern, normalized, flags=re.IGNORECASE):
            matched.append(label)

    if not matched:
        return FinancePolicyDecision(blocked=False)

    unique = tuple(dict.fromkeys(matched))
    return FinancePolicyDecision(
        blocked=True,
        reason=(
            "MVP에서는 결제, 송금, 주문, 매매, 리밸런싱처럼 돈을 이동시키거나 "
            "금융 의무를 만드는 작업을 실행하거나 준비하지 않습니다. "
            "주식/시장 정보는 조회와 브리핑만 가능합니다."
        ),
        matched_terms=unique,
    )


def is_readonly_finance_request(text: str) -> bool:
    lowered = text.lower()
    finance_terms = ("주식", "시세", "종목", "stock", "quote", "market")
    return any(term in lowered for term in finance_terms) and any(hint in lowered for hint in ALLOWED_READONLY_HINTS)
