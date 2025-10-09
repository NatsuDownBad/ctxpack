"""Importance-based pruning: remove least important messages."""
from ctxpack.utils import count_tokens


def _importance_score(msg: dict, position: int, total: int) -> float:
    """Estimate message importance. Higher = more important."""
    role = msg.get("role", "user")
    content = msg.get("content", "")

    score = 0.0
    # System messages are always important
    if role == "system":
        score += 10.0
    # Recent messages more important (recency bias)
    recency = position / max(total, 1)
    score += recency * 3.0
    # Longer messages tend to be more substantive
    length_factor = min(len(content) / 500, 2.0)
    score += length_factor
    # Messages with questions are important
    if "?" in content:
        score += 1.0
    # Assistant messages with code are important
    if role == "assistant" and ("```" in content or "def " in content):
        score += 1.5
    return score


def prune_by_importance(messages: list[dict], max_tokens: int, model: str = "gpt-4") -> list[dict]:
    """Remove least important messages to fit within budget."""
    total = sum(count_tokens(m.get("content", ""), model) for m in messages)
    if total <= max_tokens:
        return messages

    scored = []
    for i, msg in enumerate(messages):
        s = _importance_score(msg, i, len(messages))
        scored.append((i, msg, s))

    # Sort by importance (ascending) so we can drop lowest first
    scored.sort(key=lambda x: x[2])

    removed = set()
    current = total
    for idx, msg, score in scored:
        if current <= max_tokens:
            break
        tokens = count_tokens(msg.get("content", ""), model)
        removed.add(idx)
        current -= tokens

    return [msg for i, msg in enumerate(messages) if i not in removed]

