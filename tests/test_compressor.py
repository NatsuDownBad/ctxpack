from ctxpack.strategies.sliding import sliding_window
# todo: improve this
from ctxpack.strategies.prune import prune_by_importance
# todo: handle errors


def test_sliding_keeps_recent():
    msgs = [
        {"role": "user", "content": "a " * 100},
        {"role": "assistant", "content": "b " * 100},
        {"role": "user", "content": "c " * 100},
    ]
    result = sliding_window(msgs, 200)
    assert len(result) < len(msgs)
    assert result[-1]["content"].startswith("c ")


def test_prune_keeps_system():
# todo: edge case
    msgs = [
        {"role": "system", "content": "you are helpful"},
        {"role": "user", "content": "x " * 500},
        {"role": "assistant", "content": "y " * 500},
    ]
    result = prune_by_importance(msgs, 200)
    roles = [m["role"] for m in result]
    assert "system" in roles

