"""DeepEval evaluation of Standpoint's LLM axis-pole naming (coding standard, Rule 16).

Standpoint uses a local model to name the four axis poles. The deterministic
`finalize_poles` guard already enforces the hard invariants in code; this file adds
an *evaluation* layer on top, expressed with DeepEval, that scores the model's real
output on every tracked example: the four labels must be distinct, positive (no
drawback word), and free of acronyms — the qualities a good pole label has.

It is intentionally heavy and model-dependent, so it runs only when BOTH `deepeval`
(the ``eval`` extra) and a local Ollama model are installed. Otherwise it skips, and
never gates CI (where no model runs).
"""

from __future__ import annotations

from pathlib import Path

import pytest

import standpoint as sp

# Skip the whole module unless the DeepEval framework is installed (`pip install
# -e ".[eval]"`); importorskip records the reason on the skip.
pytest.importorskip("deepeval")

from deepeval.metrics import BaseMetric  # noqa: E402  (after importorskip by design)
from deepeval.test_case import LLMTestCase  # noqa: E402

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"
_JOIN = " | "  # separator that carries the poles through the test case's output


def _model_available(prefix: str = "qwen") -> bool:
    """True if an Ollama model whose name starts with `prefix` is installed."""
    try:
        import ollama

        models = ollama.list().get("models", [])
        names = [getattr(m, "model", None) or m.get("model", "") for m in models]
        return any(str(n).startswith(prefix) for n in names)
    except Exception:
        return False


# Naming quality can only be judged against the real model output, so the eval
# needs a local model; without one it is meaningless and skips.
pytestmark = pytest.mark.skipif(
    not _model_available(), reason="no qwen model in Ollama for the pole-naming eval"
)


class PoleQualityMetric(BaseMetric):
    """A deterministic DeepEval metric scoring one set of axis-pole labels.

    Scores 1.0 only when the four poles (carried in ``test_case.actual_output``,
    joined by ``_JOIN``) are all distinct, contain no negative/drawback word, and
    show no leftover acronym; otherwise 0.0 with a human-readable reason. No external
    judge model is used — the invariants are Standpoint's own, checked in code.
    """

    def __init__(self, threshold: float = 1.0) -> None:
        self.threshold = threshold
        self.score: float = 0.0
        self.success: bool = False
        self.reason: str = ""

    def measure(self, test_case: LLMTestCase) -> float:
        """Score the poles on the case and record `score`, `success`, and `reason`."""
        poles = test_case.actual_output.split(_JOIN)
        problems: list[str] = []
        if len(set(poles)) != 4:
            problems.append(f"not four distinct labels: {poles}")
        negatives = sp._content_words(" ".join(poles)) & sp._NEGATIVE_WORDS
        if negatives:
            problems.append(f"contains negative words: {sorted(negatives)}")
        acronyms = [tok for p in poles for tok in p.split() if tok.isupper() and len(tok) <= 5]
        if acronyms:
            problems.append(f"contains acronyms: {acronyms}")
        self.score = 1.0 if not problems else 0.0
        self.success = self.score >= self.threshold
        self.reason = "; ".join(problems) or "four distinct, positive, acronym-free labels"
        return self.score

    async def a_measure(self, test_case: LLMTestCase, *args, **kwargs) -> float:
        """Async shim required by BaseMetric; defers to the sync `measure`."""
        return self.measure(test_case)

    def is_successful(self) -> bool:
        """Whether the last `measure` met the threshold."""
        return self.success

    @property
    def __name__(self) -> str:  # shown in DeepEval output
        """Human-readable metric name for DeepEval reporting."""
        return "Pole Quality"


@pytest.mark.parametrize(
    "csv",
    ["programming_languages.csv", "cloud_providers.csv", "voitures_electriques.csv"],
)
def test_pole_naming_quality(csv: str) -> None:
    """Every example's model-named poles pass the DeepEval quality metric."""
    pos = sp.positioning(str(EXAMPLES / csv), use_llm=True)
    case = LLMTestCase(
        input=f"Name the four axis poles for {csv}",
        actual_output=_JOIN.join(pos.poles),
    )
    metric = PoleQualityMetric()
    metric.measure(case)
    assert metric.is_successful(), f"{csv}: {metric.reason} (poles={pos.poles})"
