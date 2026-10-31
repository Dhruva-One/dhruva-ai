from pathlib import Path

_TEMPLATES = Path(__file__).parent / "templates"


def load_prompt(name: str, version: int = 1) -> str:
    """Prompts are versioned files; every change is checked by the evaluation suite before release."""
    return (_TEMPLATES / f"{name}.v{version}.txt").read_text(encoding="utf-8")
