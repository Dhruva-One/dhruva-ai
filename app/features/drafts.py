from pydantic import BaseModel, Field

from app.metering.meter import CostMeter
from app.prompts.registry import load_prompt
from app.providers.base import ModelProvider


class NoticeDraftRequest(BaseModel):
    tenant_id: str
    audience: str = Field(examples=["Parents of Class 10"])
    facts: list[str] = Field(min_length=1)
    language: str = Field(default="en", pattern="^(en|hi)$")


class Draft(BaseModel):
    text: str
    model: str
    needs_approval: bool = True  # Dhruva drafts, a person approves.


def draft_notice(req: NoticeDraftRequest, provider: ModelProvider, meter: CostMeter) -> Draft:
    meter.check(req.tenant_id)
    prompt = load_prompt("notice_draft").format(
        language=req.language, audience=req.audience, facts="\n".join(f"- {f}" for f in req.facts)
    )
    out = provider.complete(prompt)
    meter.record(req.tenant_id, "notice_draft", out.cost_cents)
    return Draft(text=out.text, model=out.model)
