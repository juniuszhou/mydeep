"""Command-line entrypoint for the simple DeepAgents dispatcher."""

from __future__ import annotations

import argparse
from collections.abc import Sequence
from typing import Any

from mydeep.agent import DEFAULT_MODEL, create_agent


def _message_content(message: Any) -> Any:
    if isinstance(message, dict):
        return message.get("content")
    return getattr(message, "content", None)


def _content_to_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
        return "\n".join(part for part in parts if part)
    return ""


def _last_response_text(result: dict[str, Any]) -> str:
    for message in reversed(result.get("messages", [])):
        text = _content_to_text(_message_content(message))
        if text:
            return text
    return str(result)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the mydeep dispatcher deepagent.",
    )
    parser.add_argument("prompt", help="Task for the dispatcher to complete.")
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Model identifier to use. Defaults to {DEFAULT_MODEL}.",
    )
    args = parser.parse_args(argv)

    agent = create_agent(model=args.model)
    result = agent.invoke({"messages": [{"role": "user", "content": args.prompt}]})
    print(_last_response_text(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
