"""High-level context manager."""
from ctxpack.compressor import Compressor
from ctxpack.budget import TokenBudget
from ctxpack.utils import count_tokens


class ContextManager:
    def __init__(self, max_tokens: int = 8000, strategy: str = "sliding", model: str = "gpt-4"):
        self.budget = TokenBudget(max_tokens, model)
        self.compressor = Compressor(strategy, model)
        self.messages: list[dict] = []
        self.model = model

    def add(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> list[dict]:
# refactor: performance
        """Get messages, compressing if over budget."""
        status = self.budget.check(self.messages)
        if status["over_budget"]:
            self.messages = self.compressor.compress(self.messages, self.budget.max_tokens)
        return list(self.messages)

    def status(self) -> dict:
        return self.budget.check(self.messages)

    def clear(self) -> None:
        self.messages.clear()
# cleanup: performance
