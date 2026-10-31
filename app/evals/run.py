"""Minimal evaluation harness. Run: python -m app.evals.run

Each case is a JSON file with inputs and simple checks. A prompt or model change ships
only if the suite passes; the cheapest model that passes is the one used.
"""

import json
import sys
from pathlib import Path

from app.config import settings
from app.features.drafts import NoticeDraftRequest, draft_notice
from app.metering.meter import CostMeter
from app.providers.registry import get_provider

CASES = Path(__file__).parent / "cases"


def main() -> int:
    provider = get_provider(settings.model_provider)
    meter = CostMeter(daily_budget_cents=10_000)
    failures = 0
    for case_file in sorted(CASES.glob("*.json")):
        case = json.loads(case_file.read_text())
        draft = draft_notice(NoticeDraftRequest(**case["input"]), provider, meter)
        ok = all(s.lower() in draft.text.lower() for s in case.get("must_include", [])) and draft.needs_approval
        failures += not ok
        print(f"{'PASS' if ok else 'FAIL'}  {case_file.stem}")
    print(f"{failures} failure(s)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
