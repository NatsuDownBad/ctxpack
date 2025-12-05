# ctxpack

Context window compression and management for LLM conversations. Strategies: sliding window, importance-based pruning, recursive summarization.

## Install

```
pip install -e .
```

## Usage

```python
from ctxpack import ContextManager

ctx = ContextManager(max_tokens=4000, strategy="sliding")
ctx.add("system", "you are helpful")
ctx.add("user", "hello")
ctx.add("assistant", "hi there")

messages = ctx.get_messages()  # auto-compresses if over budget
print(ctx.status())
```

## License

MIT
