"""Basic LangChain setup."""

from pathlib import Path

from deepagents import create_deep_agent
from langchain_ollama import ChatOllama

PROJECT_ROOT = Path("/home/junius/github/junius/mydeep")

llm = ChatOllama(
    model="gemma4:e2b",
    temperature=0,
    num_ctx=8192,
)

# without backend, so it can not write files
agent = create_deep_agent(
    model="ollama:gemma4:e2b",
)


# agent = create_deep_agent(
#     model="ollama:gemma4:e2b",
#     backend=LocalShellBackend(
#         root_dir=PROJECT_ROOT, virtual_mode=True, env={"PATH": "/usr/bin:/bin"}
#     ),
#     system_prompt=(
#         "Use the available write_file tool to create files. "
#         "The file path argument is named file_path."
#     ),
# )

# agent = create_deep_agent(
#     model="ollama:gemma4:e2b",
#     backend=SandboxBackend(),
# )

# agent = create_deep_agent(
#     model=llm,
#     backend=FilesystemBackend(root_dir=PROJECT_ROOT, virtual_mode=True),
#     system_prompt=(
#         "Use the available write_file tool to create files. "
#         "The file path argument is named file_path."
#     ),
# )

result = agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "Create test.txt in current directory with exactly this content: Hello, world!",
            }
        ]
    }
)
for message in result["messages"]:
    print(message.content)
