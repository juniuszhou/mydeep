# langchain deepagent

This project defines a small DeepAgents dispatcher. The main agent breaks a
request into subtasks and delegates them through DeepAgents' built-in `task`
tool to specialized subagents.

## install

```shell
uv tool install 'deepagents-cli[ollama,groq]'
uv sync
```

If you are not using `uv`, install the package in editable mode:

```shell
python -m pip install -e .
```

## config
~/.deepagents/.env

Set the API key required by the model in `deepagents.toml`. The default model is
`anthropic:claude-sonnet-4-6`, so Anthropic users should set:

```shell
ANTHROPIC_API_KEY=...
```

## run

```shell
uv run mydeep "Research the topic, propose an implementation, review risks, and write a short summary."
```

Or:

```shell
python -m mydeep "Plan a small FastAPI app and review the security risks."
```

## subagents

- `researcher`: fact-finding, comparisons, and open questions.
- `implementer`: code changes, APIs, examples, and implementation plans.
- `reviewer`: bugs, risks, edge cases, and missing tests.
- `writer`: final summaries, docs, changelogs, and polished prose.
