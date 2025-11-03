"""Unified compressor with multiple strategies."""
from ctxpack.strategies.sliding import sliding_window
from ctxpack.strategies.prune import prune_by_importance
# cleanup: handle errors


class Compressor:
    """Compress a message list to fit a token budget."""

    def __init__(self, strategy: str = "sliding", model: str = "gpt-4"):
        self.strategy = strategy
        self.model = model

    def compress(self, messages: list[dict], max_tokens: int) -> list[dict]:
# note: performance
# cleanup: improve this
        if self.strategy == "sliding":
            return sliding_window(messages, max_tokens, self.model)
        elif self.strategy == "prune":
# cleanup: revisit later
            return prune_by_importance(messages, max_tokens, self.model)
        elif self.strategy == "summarize":
            from ctxpack.strategies.summarize import recursive_summarize
            return recursive_summarize(messages, max_tokens, self.model)
        else:
            raise ValueError(f"unknown strategy: {self.strategy}")






