"""DeepAgents dispatcher with specialized subagents."""

from __future__ import annotations

from typing import Any

from deepagents import create_deep_agent

DEFAULT_MODEL = "gemma4:e4b"

DISPATCHER_PROMPT = """You are my-agent, an orchestration-focused deepagent.

Your main job is to break user requests into clear subtasks, dispatch those
subtasks to the best specialized subagent with the task tool, and synthesize the
results into one useful answer.

Dispatch guidance:
- Use researcher for fact-finding, background reading, comparisons, and unknowns.
- Use implementer for code changes, implementation plans, APIs, and examples.
- Use reviewer for critique, risks, bugs, edge cases, and missing tests.
- Use writer for final summaries, documentation, release notes, and polishing.

When subtasks are independent, call multiple subagents so they can work in
parallel from clean contexts. Give each subagent a specific objective and ask it
to return only the important findings. Combine their outputs, resolve conflicts,
and be explicit about any uncertainty.
"""


def classify_work(task: str) -> str:
    """Suggest which subagent should handle a task."""
    lowered = task.lower()
    if any(word in lowered for word in ("bug", "risk", "review", "test", "edge")):
        return "reviewer"
    if any(word in lowered for word in ("write", "doc", "summary", "explain")):
        return "writer"
    if any(word in lowered for word in ("implement", "code", "api", "build", "fix")):
        return "implementer"
    if any(word in lowered for word in ("research", "compare", "find", "learn")):
        return "researcher"
    return "researcher"


def make_checklist(goal: str) -> list[str]:
    """Create a short execution checklist for a goal."""
    return [
        f"Clarify the desired outcome for: {goal}",
        "Identify the smallest useful units of work.",
        "Delegate specialized pieces to the right subagents.",
        "Merge the returned findings into a single answer.",
        "Call out open questions, risks, or follow-up work.",
    ]


def summarize_text(text: str, max_words: int = 80) -> str:
    """Return a compact first-pass summary of text."""
    words = text.split()
    if len(words) <= max_words:
        return text
    return " ".join(words[:max_words]).rstrip() + "..."


def review_risks(change: str) -> list[str]:
    """List common review risks for a proposed change."""
    return [
        f"Does the change satisfy the requested behavior: {change}",
        "Are errors and empty inputs handled intentionally?",
        "Are external side effects, secrets, and permissions controlled?",
        "Is there focused test coverage for the highest-risk behavior?",
    ]


SUBAGENTS: list[dict[str, Any]] = [
    {
        "name": "researcher",
        "description": (
            "Use for fact-finding, background research, comparisons, and open "
            "questions that need careful investigation."
        ),
        "system_prompt": (
            "You are a focused research subagent. Gather relevant facts, separate "
            "confirmed information from assumptions, and return concise findings "
            "with any important caveats."
        ),
        "tools": [summarize_text],
    },
    {
        "name": "implementer",
        "description": (
            "Use for coding tasks, implementation plans, API design, examples, "
            "and step-by-step build work."
        ),
        "system_prompt": (
            "You are a pragmatic implementation subagent. Turn requirements into "
            "small concrete steps, prefer simple designs, and mention files, APIs, "
            "or tests that should change."
        ),
        "tools": [make_checklist],
    },
    {
        "name": "reviewer",
        "description": (
            "Use for code review, bug hunting, risk analysis, edge cases, and "
            "test coverage gaps."
        ),
        "system_prompt": (
            "You are a critical review subagent. Prioritize correctness, security, "
            "operational risk, and missing tests. Return findings ordered by "
            "severity and skip low-value style comments."
        ),
        "tools": [review_risks],
    },
    {
        "name": "writer",
        "description": (
            "Use for final summaries, documentation, changelog entries, release "
            "notes, and polishing rough notes into clear prose."
        ),
        "system_prompt": (
            "You are a concise writing subagent. Convert rough material into clear, "
            "structured prose that preserves technical accuracy and avoids fluff."
        ),
        "tools": [summarize_text],
    },
]


def create_agent(model: str | None = None):
    """Create the dispatcher deepagent."""
    return create_deep_agent(
        model=model or DEFAULT_MODEL,
        tools=[classify_work, make_checklist],
        system_prompt=DISPATCHER_PROMPT,
        subagents=SUBAGENTS,
        name="my-agent",
    )
