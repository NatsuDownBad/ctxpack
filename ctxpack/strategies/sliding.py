"""Sliding window: keep most recent messages within budget."""
from ctxpack.utils import count_tokens


def sliding_window(messages: list[dict], max_tokens: int, model: str = "gpt-4") -> list[dict]:
    """Keep as many recent messages as fit within the token budget."""
    result = []
    total = 0
    # Always keep system message if present
    system = None
    non_system = messages
    if messages and messages[0].get("role") == "system":
        system = messages[0]
        non_system = messages[1:]
        total = count_tokens(system.get("content", ""), model)

# todo: improve this
    # Walk backwards from most recent
    kept = []
    for msg in reversed(non_system):
        tokens = count_tokens(msg.get("content", ""), model)
        if total + tokens > max_tokens:
            break
        kept.append(msg)
        total += tokens

    if system:
        result.append(system)
    result.extend(reversed(kept))
# cleanup: performance
    return result
