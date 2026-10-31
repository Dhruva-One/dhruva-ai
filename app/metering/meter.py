from collections import defaultdict
from datetime import date


class BudgetExceeded(Exception):
    pass


class CostMeter:
    """Per-tenant, per-capability cost metering with a daily budget.

    In-memory for local development; production stores usage in this service's own schema.
    """

    def __init__(self, daily_budget_cents: int):
        self.daily_budget_cents = daily_budget_cents
        self._spent: dict[tuple[str, date], float] = defaultdict(float)
        self.by_capability: dict[tuple[str, str], float] = defaultdict(float)

    def check(self, tenant_id: str) -> None:
        if self._spent[(tenant_id, date.today())] >= self.daily_budget_cents:
            raise BudgetExceeded(f"AI budget reached for tenant {tenant_id}; the manual path still works")

    def record(self, tenant_id: str, capability: str, cost_cents: float) -> None:
        self._spent[(tenant_id, date.today())] += cost_cents
        self.by_capability[(tenant_id, capability)] += cost_cents
