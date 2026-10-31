from app.providers.base import Completion, ModelProvider


class FakeProvider(ModelProvider):
    """Offline provider for local development and tests. Returns a deterministic draft."""

    name = "fake"

    def complete(self, prompt: str, *, max_tokens: int = 512) -> Completion:
        first_line = prompt.strip().splitlines()[-1][:200] if prompt.strip() else ""
        text = f"[draft] {first_line}"
        return Completion(text=text, model="fake-1", input_tokens=len(prompt) // 4,
                          output_tokens=len(text) // 4, cost_cents=0.0)
