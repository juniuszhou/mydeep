"""Basic LangChain setup."""

import os
from pprint import pprint

from deepagents import AsyncSubAgent, create_deep_agent
from langchain_openai import ChatOpenAI

# Set up local LLM (Ollama endpoint)
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_KEY"] = "ollama"  # Dummy key; Ollama doesn't need a real one

llm = ChatOpenAI(
    model="gemma4:e2b",
    temperature=0,
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

subagent = AsyncSubAgent(
    model="ollama:gemma4:e2b",
    tools=[],
    system_prompt="You are a helpful assistant that can answer questions and help with tasks.",
    name="basic-subagent",
    description="A helpful assistant that can answer questions and help with tasks.",
)

agent = create_deep_agent(
    model="ollama:gemma4:e2b",
    tools=[],
    subagents=[subagent],
    system_prompt="You are an agent manager to coordinate and assign take to your subagents.",
    name="basic-agent",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What is the capital of France?"}]}
)
for message in result["messages"]:
    pprint(message.content)
