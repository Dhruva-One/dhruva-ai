from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Completion:
    text: str
    model: str
    input_tokens: int
    output_tokens: int
    cost_cents: float


class ModelProvider(ABC):
    """Swappable model provider.

    Implementations must keep inference in an India region whenever the prompt holds
    student or staff data, and report token usage so cost can be metered per tenant.
    """

    name: str

    @abstractmethod
    def complete(self, prompt: str, *, max_tokens: int = 512) -> Completion: ...
