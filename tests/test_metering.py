import pytest

from app.metering.meter import BudgetExceeded, CostMeter


def test_budget_blocks_after_limit():
    m = CostMeter(daily_budget_cents=10)
    m.record("t1", "notice_draft", 10)
    with pytest.raises(BudgetExceeded):
        m.check("t1")
    m.check("t2")  # other tenants unaffected
