from fastapi import FastAPI, HTTPException

from app.config import settings
from app.features.drafts import Draft, NoticeDraftRequest, draft_notice
from app.features.seating import SeatingPlan, SeatingRequest, plan_seating
from app.metering.meter import BudgetExceeded, CostMeter
from app.providers.registry import get_provider
from app.spec_stubs import register_spec_stubs

app = FastAPI(title="dhruva-ai", version="0.1.0")
provider = get_provider(settings.model_provider)
meter = CostMeter(settings.default_tenant_daily_budget_cents)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "dhruva-ai", "provider": provider.name, "region": settings.inference_region}


@app.post("/v1/drafts/notice", response_model=Draft)
def notice_draft(req: NoticeDraftRequest) -> Draft:
    try:
        return draft_notice(req, provider, meter)
    except BudgetExceeded as exc:
        # Shed, never block: the person can still write the notice by hand.
        raise HTTPException(status_code=429, detail=str(exc)) from exc


@app.post("/v1/exams/seating", response_model=SeatingPlan)
def exam_seating(req: SeatingRequest) -> SeatingPlan:
    try:
        return plan_seating(req)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


# Every AI-service API from the functional spec that is not implemented above answers 501 (see app/spec_stubs.py).
spec_coverage = register_spec_stubs(app)


@app.get("/internal/spec/coverage")
def coverage() -> dict:
    return spec_coverage
