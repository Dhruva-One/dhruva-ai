from app.providers.base import ModelProvider
from app.providers.fake import FakeProvider

# Real providers (for example Amazon Bedrock in ap-south-1) are added here once the
# India-region availability check in the Technology doc is complete.
_PROVIDERS: dict[str, type[ModelProvider]] = {"fake": FakeProvider}


def get_provider(name: str) -> ModelProvider:
    try:
        return _PROVIDERS[name]()
    except KeyError as exc:
        raise ValueError(f"Unknown model provider '{name}'. Known: {sorted(_PROVIDERS)}") from exc
