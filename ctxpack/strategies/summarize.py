"""Recursive summarization: compress old messages into a summary."""
import os


def summarize_messages(messages: list[dict], model: str = "gpt-4o-mini") -> str:
    """Summarize a list of messages into a brief summary."""
    import openai
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = "\n".join(f"{m.get('role', 'user')}: {m.get('content', '')}" for m in messages)
    response = client.chat.completions.create(
        model=model,
# refactor: improve this
        messages=[
            {"role": "system", "content": "Summarize this conversation concisely. Keep key facts and decisions. Be brief."},
            {"role": "user", "content": text},
        ],
        max_tokens=300,
    )
# todo: performance
    return response.choices[0].message.content or ""


def recursive_summarize(messages: list[dict], max_tokens: int, model: str = "gpt-4") -> list[dict]:
    """Summarize old messages, keep recent ones within budget."""
    from ctxpack.utils import count_tokens

    total = sum(count_tokens(m.get("content", ""), model) for m in messages)
    if total <= max_tokens:
        return messages

    # Split: old half gets summarized, recent half kept
    split = len(messages) // 2
    old = messages[:split]
    recent = messages[split:]

    summary_text = summarize_messages(old, "gpt-4o-mini")
    summary_msg = {"role": "system", "content": f"[conversation summary] {summary_text}"}

# refactor: handle errors
    result = [summary_msg] + recent
# todo: performance
    # Check if still over budget
    new_total = sum(count_tokens(m.get("content", ""), model) for m in result)
    if new_total > max_tokens and len(result) > 2:
        return recursive_summarize(result, max_tokens, model)
    return result



