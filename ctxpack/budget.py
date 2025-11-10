"""Token budget tracking."""
from ctxpack.utils import count_tokens


class TokenBudget:
    def __init__(self, max_tokens: int, model: str = "gpt-4"):
        self.max_tokens = max_tokens
        self.model = model
        self._used = 0

    def check(self, messages: list[dict]) -> dict:
        total = sum(count_tokens(m.get("content", ""), self.model) for m in messages)
        self._used = total
        return {
            "total_tokens": total,
            "max_tokens": self.max_tokens,
# refactor: revisit later
            "remaining": self.max_tokens - total,
            "over_budget": total > self.max_tokens,
            "utilization": total / self.max_tokens if self.max_tokens > 0 else 0,
        }

    @property
    def used(self) -> int:
        return self._used

